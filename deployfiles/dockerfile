FROM node:16.14.2 AS front_build_base
WORKDIR /Project/Front
ENV FRONT_NAME=Editor
# RUN rm package-lock.json

COPY ./Editor/package.json package.json
RUN npm config set registry https://registry.npm.taobao.org/ && \
    yarn config set registry https://registry.npm.taobao.org/ && \
    yarn

COPY ./Editor/  .
RUN npm run build

FROM python:3.6.5-slim AS back_deploy_base
WORKDIR /Project/Back
ENV BACK_NAME=GIT_INTERACT

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

# apt-get换源

# 不同版本号源不一样 cat /etc/os-release
# 1：# docker内sourcelist换源：https://blog.csdn.net/weixin_38556197/article/details/128139108
# RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
# or 2： https://blog.csdn.net/qq_36973540/article/details/125960846
# 2023年4月后，国内镜像源全部把stretch（9）版本归档为过气版本，因此镜像源url发生变化
RUN echo > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-archive/debian/ stretch main non-free contrib \ndeb-src http://mirrors.aliyun.com/debian-archive/debian/ stretch main non-free contrib \ndeb http://mirrors.aliyun.com/debian-archive/debian-security/ stretch/updates main\ndeb-src http://mirrors.aliyun.com/debian-archive/debian-security/ stretch/updates main\ndeb http://mirrors.aliyun.com/debian-archive/debian/ stretch-proposed-updates main non-free contrib \ndeb-src http://mirrors.aliyun.com/debian-archive/debian/ stretch-proposed-updates main non-free contrib \ndeb http://mirrors.aliyun.com/debian-archive/debian/ stretch-backports main non-free contrib \ndeb-src http://mirrors.aliyun.com/debian-archive/debian/ stretch-backports main non-free contrib" > /etc/apt/sources.list
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
#     echo "deb http://mirrors.aliyun.com/debian-archive/debian-security// squeeze/updates main non-free contrib" >> /etc/apt/sources.list && \
#     echo "deb-src http://mirrors.aliyun.com/debian-archive/debian-security// squeeze/updates main non-free contrib" >> /etc/apt/sources.list

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

# 把后端项目的requirements文件移入并pip install
COPY ./GIT_INTERACT/requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 把后端项目文件挪入镜像
COPY ./GIT_INTERACT/ .
# 将前端打包出来的文件放入后端相应位置
# 前端构建的css和js文件夹放static文件夹下
COPY --from=front_build_base /Project/Front/build/static/css ./static/css
COPY --from=front_build_base /Project/Front/build/static/js ./static/js
# 前端构建的其他文件放templates文件夹下
COPY --from=front_build_base /Project/Front/build ./templates

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