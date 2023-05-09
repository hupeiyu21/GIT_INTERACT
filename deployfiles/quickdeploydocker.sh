# 构建镜像，其中--rm参数决定是否删除中间层
DOCKER_BUILDKIT=0 && docker build --rm=false -t "flaskgitmanageimagequick" -f ./quickdeploydocker .

# 暂停并删除以前的容器
echo "stop and remove previous container"
docker stop $(docker ps -a | grep "flaskgitmanagecontainquick" | awk '{print $1 }') || true
docker rm $(docker ps -a | grep "flaskgitmanagecontainquick" | awk '{print $1 }') || true

echo "start to run this container(id):"
# 启动容器
# 挂载docker到容器内
docker run --name flaskgitmanagecontainquick -d -p 30007:5000 -v /var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker flaskgitmanageimagequick

# 等待任意按键输入，保持shell窗口
echo "Finish, please Visit port 30007, you can enter any key to exit:"
read -n 1