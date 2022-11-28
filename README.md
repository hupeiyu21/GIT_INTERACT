# 运行

1. 命令行使用 `pip install -r requirements.txt` 下载所需模块
2. cd到`04managegit.py`所在目录下,运行 `python 04managegit.py` 

默认项目存储文件夹设置在与python文件同目录下

默认基地址为 `http://127.0.0.1:5000`

请求类型都为POST请求，请求参数类型见`media type`

# 接口


见链接: `https://www.apifox.cn/apidoc/shared-551b58ad-5b92-418a-aa3a-08cbda86a84c`

访问密码 : FYP2022

## 接口参数说明

repodir: git仓库的克隆地址 目前http和ssh都可以

reponame: 调用`repo/clone`或`repo/checkout`后返回的json里'foldertree'里最外部的'name'（也就是克隆下来的项目文件夹名）

hash: 某一次commit时的哈希值，在`repo/clone`的响应的'logs'里

file_rel_path\folder_rel_path: 相对路径，在`repo clone`或`repo/checkout`或`show/folderplane`的响应的"foldertree"里的"rel_path"

file_content: 上传的某个完整文件内容（formdata形式的file）




