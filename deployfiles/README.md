# 部署 在线编辑GIT 这个项目的前后端

## 部署前的小提示

1. 注意前端请求的基地址（src/api/ajax.js)的BASEURL应当为服务器外网地址，如（http://114.115.249.201:30004/）
2. 宿主机里的前端文件不用包含node_modules文件夹
3. 宿主机安装git和docker
4. shell的换行符应当为\n（LF格式）
5. id_rsa文件是私钥文件，不要把它放在公开的存储库里

## 文件目录结构

- Editor（前端项目）
- GIT_INTERACT（后端项目）
- deploy.sh（一键打包部署的shell）
- dockerfile（用于打包部署的docker文件）
- makeimage.sh（一键打包的shell）
- makeimage（用于打包的docker文件）
- quickdeploydocker.sh（一键部署的shell）
- quickdeploydocker（用于部署的docker文件）
- id_rsa（用于项目的ssh密钥）
- README.md（本文档）

## （方法1，需要python）使用CLI

1. 将ssh私钥(id_rsa文件)，放置在与这个README同级目录下。在需要被修改的用户的git项目里设置对应的公钥。
2. 将本项目配套的dockerfile，放置在与这个README同级目录下。
3. 将前端项目文件夹Editor放在与这个README同级目录下。
3. 将后端项目文件夹GIT_INTERACT放在与这个README同级目录下。
4. 在这个README所在目录下执行 `docker build -t "flask_gitmanage_image" .`来构建镜像
5. （可跳过）使用`docker images`查看所有镜像，其中应该有flask_gitmanage_image
6. 启动容器：`docker run --name flask_gitmanage_contain -d -p 30004:5000 flask_gitmanage_image`其中，-d表示以守护进程启动

## （方法2，需要docker）使用shell脚本

1. 这个方法需要从头初始化项目环境和安装第三方库和打包代码，耗时长
2. 将ssh私钥(id_rsa文件)，放置在与这个README同级目录下。在需要被修改的用户的git项目里设置对应的公钥。
3. 将dockerfile和deploy.sh，放置在与这个README同级目录下。
4. 运行:`bash deploy.sh`，这会新建一个名为flaskgitmanageimageyusen的镜像，并容器化它

## （方法3，需要docker）使用docker预打包镜像

1. 这个方法就是从镜像库里拉取我预打包的镜像，耗时短
2. 将ssh私钥(id_rsa文件)，放置在与这个README同级目录下。在需要被修改的用户的git项目里设置对应的公钥。
3. 将quickdeploydocker和quickdeploydocker.sh，放置在与这个README同级目录下。
4. 运行:`bash quickdeploydocker.sh`，这会新建一个名为flaskgitmanageimagequick的镜像，并容器化它

# 预打包（需要docker）

将项目环境和第三方库和当前版本的代码打包成镜像，后面运行只用配置ssh key

1. 这个方法需要从头初始化项目环境和安装第三方库和打包代码，耗时长
2. 将makeimage和makeimage.sh，放置在与这个README同级目录下。
3. 运行:`bash makeimage.sh`，这会新建一个名为sanmusen214/xjtlu-fyp-yusen的镜像