# 当前时间戳(秒)
timestamp=`date '+%s'`
echo "time stamp: $TIMESTAMP"

# 前端仓库名
FRONT_NAME="Editor"
# 后端仓库名
BACK_NAME="GIT_INTERACT"

git config --global --unset http.proxy
git config --global --unset https.proxy
git config --global --unset http.https://github.com.proxy


# 拉取镜像，|| true表示如果存储库已存在，则忽略clone的报错
# 使用仓库的http链接
# clone也可手动提前进行，或通过FTP把项目传到宿主机上
git clone https://github.com/sanmusen214/GIT_INTERACT.git || true
git clone https://github.com/zhyAmber/Editor.git || true

# 把仓库更新
cd ./$FRONT_NAME
git pull || true
cd ../$BACK_NAME
git pull || true
cd ../

# 构建镜像，其中--rm参数决定是否删除中间层
DOCKER_BUILDKIT=0 && docker build --rm=false -t "flaskgitmanageimage$TIMESTAMP" .

# 暂停并删除以前的容器
echo "stop and remove previous container"
docker stop $(docker ps -a | grep "flaskgitmanagecontain" | awk '{print $1 }') || true
docker rm $(docker ps -a | grep "flaskgitmanagecontain" | awk '{print $1 }') || true

echo "start to run this container(id):"
# 启动容器
docker run --name flaskgitmanagecontain -d -p 30004:5000 flaskgitmanageimage$TIMESTAMP

# 等待任意按键输入，保持shell窗口
echo "Finish, time stamp is $TIMESTAMP, you can enter any key to exit:"
read -n 1