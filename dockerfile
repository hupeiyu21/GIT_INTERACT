FROM python:3.6.5-slim
WORKDIR /Project/GITCONTROL

COPY requirements.txt ./
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


# apt-get换源
# 不同版本号源不一样 RUN cat /etc/os-release
# 1：# docker内sourcelist换源：https://blog.csdn.net/weixin_38556197/article/details/128139108
# RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
# or 2： https://blog.csdn.net/qq_36973540/article/details/125960846
RUN echo > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ stretch main non-free contrib \ndeb-src http://mirrors.aliyun.com/debian/ stretch main non-free contrib \ndeb http://mirrors.aliyun.com/debian-security stretch/updates main \ndeb-src http://mirrors.aliyun.com/debian-security stretch/updates main \ndeb http://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib \ndeb-src http://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib \ndeb http://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib \ndeb-src http://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib" > /etc/apt/sources.list
# or 3：# 阿里开源站（Debian和Debian security）：https://developer.aliyun.com/mirror/?serviceType=&tag=&keyword=debian
# RUN echo > /etc/apt/sources.list && \
#     echo "deb https://mirrors.aliyun.com/debian/ stretch main non-free contrib" >> /etc/apt/sources.list && \
#     echo "deb-src https://mirrors.aliyun.com/debian/ stretch main non-free contrib" >> /etc/apt/sources.list && \
#     echo "deb https://mirrors.aliyun.com/debian-security stretch/updates main" >> /etc/apt/sources.list && \
#     echo "deb-src https://mirrors.aliyun.com/debian-security stretch/updates main" >> /etc/apt/sources.list && \
#     echo "deb https://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib" >> /etc/apt/sources.list && \
#     echo "deb-src https://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib" >> /etc/apt/sources.list && \
#     echo "deb https://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib" >> /etc/apt/sources.list && \
#     echo "deb-src https://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib" >> /etc/apt/sources.list && \
#     echo "deb http://mirrors.aliyun.com/debian-security/ squeeze/updates main non-free contrib" >> /etc/apt/sources.list && \
#     echo "deb-src http://mirrors.aliyun.com/debian-security/ squeeze/updates main non-free contrib" >> /etc/apt/sources.list

# 更新apt-get
RUN apt-get clean && \
    apt-get update && \
    apt-get upgrade -y

# 安装软件
RUN apt-get install -y git
RUN apt-get install -y redis-server
# # 验证git有效
# RUN touch /root/.ssh/known_hosts
# RUN ssh-keyscan github.org >> /root/.ssh/known_hosts
# 如果git不在系统变量中，需要手动指定
# CMD ["set","GIT_PYTHON_GIT_EXECUTABLE=C:\\git\\bin\\git.exe"]

COPY . .

# 配置ssh密钥
RUN mkdir -p /root/.ssh
COPY id_rsa /root/.ssh/
RUN echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config && \
    echo "UserKnownHostsFile /dev/null" >> /etc/ssh/ssh_config
RUN git config --global user.email "oneditor@163.com" && \
    git config --global user.name "oneditor" && \
    chown 1000:1000 /root/.ssh/id_rsa

# 启动redis, flask
# https://qa.1r1g.com/sf/ask/594675721/
CMD service redis-server start && gunicorn 04managegit:createapp\(\) -c ./gunicorn.conf.py