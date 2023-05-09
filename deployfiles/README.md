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
- deploy.sh（一键部署的shell）
- dockerfile（用于部署的docker文件）
- id_rsa（用于项目的ssh密钥）
- README.md（本文档）

## （方法1）使用CLI

1. 将ssh私钥(id_rsa文件)，放置在与这个README同级目录下。在需要被修改的用户的git项目里设置对应的公钥。
2. 将本项目配套的dockerfile，放置在与这个README同级目录下。
3. 将前端项目文件夹Editor放在与这个README同级目录下。
3. 将后端项目文件夹GIT_INTERACT放在与这个README同级目录下。
4. 在这个README所在目录下执行 `docker build -t "flask_gitmanage_image" .`来构建镜像
5. （可跳过）使用`docker images`查看所有镜像，其中应该有flask_gitmanage_image
6. 启动容器：`docker run --name flask_gitmanage_contain -d -p 30004:5000 flask_gitmanage_image`其中，-d表示以守护进程启动

## （方法2）使用shell

1. 将ssh私钥(id_rsa文件)，放置在与这个README同级目录下。在需要被修改的用户的git项目里设置对应的公钥。
2. 将dockerfile，放置在与这个README同级目录下。
3. 运行本项目配套的deploy.sh:`bash deploy.sh`，这会新建一个名为flask_gitmanage_image_{时间戳}的镜像，并容器化它

