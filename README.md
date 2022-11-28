# 运行

1. 命令行**cd到**`04managegit.py`所在目录下,使用 `pip install -r requirements.txt` 下载所需模块
2. 运行 `python 04managegit.py` 

默认项目们的存储文件夹设置在与`04managegit.py`文件同目录下，名字为storaged

默认基地址为 `http://127.0.0.1:5000`，请求该地址，后面加上接口的路由即可

请求类型都为POST请求，请求参数类型见文档（大部分都是application/x-www-form-urlencoded）

# 接口


见API文档: `https://www.apifox.cn/apidoc/shared-551b58ad-5b92-418a-aa3a-08cbda86a84c`

访问密码 : FYP2022

## 参数说明

repodir: git仓库的克隆地址 目前http和ssh都可以

reponame: 调用`/repo/clone`或`/repo/checkout`后返回的json里'foldertree'里最外部的'name'（也就是克隆下来的项目文件夹名），调用git clone后建议前端将这个存储下来

hash: 某一次commit时的哈希值，在`/repo/clone`或`/show/gitlogs`的响应的json的'logs'里

file_rel_path/folder_rel_path: 文件/文件夹的相对路径（相对于项目的文件夹），在`/repo/clone`或`/repo/checkout`或`/show/folderplane`或`/show/foldertree`的响应的"foldertree"里的每个文件/文件夹都有"rel_path"，这个经过了base64编码，所以看上去是乱码，后端传过去前端什么 前端直接原样传回后端即可（编码解码都在后端）

file_content: 上传的某个代码文件内容（formdata形式的file），前端如何发起这种请求请看API文档里的"示例代码"




