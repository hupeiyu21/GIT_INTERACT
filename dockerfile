FROM python:3.8-slim
WORKDIR /Project/GITCONTROL

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


# apt-get换源：https://blog.csdn.net/weixin_38556197/article/details/128139108
# 版本号 RUN cat /etc/os-release
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
    apt-get clean && \
    apt-get update && \
    apt-get upgrade -y
RUN apt-get install -y git
RUN apt-get install -y redis-server
# # 验证git有效
# RUN touch /root/.ssh/known_hosts
# RUN ssh-keyscan github.org >> /root/.ssh/known_hosts
# 如果git不在系统变量中，需要手动指定
# CMD ["set","GIT_PYTHON_GIT_EXECUTABLE=C:\\git\\bin\\git.exe"]

COPY . .

# 启动flask
CMD ["service","redis-server","start"]
# https://qa.1r1g.com/sf/ask/594675721/
CMD ["gunicorn", "04managegit:createapp()", "-c", "./gunicorn.conf.py"]