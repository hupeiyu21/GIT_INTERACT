import subprocess
import os
import re
from flask import Flask, jsonify, request, abort, Response, render_template, send_from_directory
from flask_cors import CORS
import base64

localstore=os.path.join(os.path.split(__file__)[0],"storaged")
if not os.path.exists(localstore):
    os.mkdir(localstore)
# relpath: 相对于项目文件夹的相对路径, base64
# abspath：全局路径


def clone(repo, dir):
    '''
    远端仓库地址和保存至本地哪个文件夹下
    '''
    ret, out = subprocess.getstatusoutput(
        'cd {} && git clone {}'.format(dir, repo))
    if ret == 128 or ret == 0:
        aind = out.find("'")
        bind = out.rfind("'")
        # print(ret)
        return {'status': 200, 'reponame': out[aind+1:bind]}
    return {'status': 400, 'info': out}


def checkout(dir, hashcode):
    """
    通过git切换版本
    """
    ret, out = subprocess.getstatusoutput(
        'cd {} && git checkout 1>nul 2>nul {}'.format(dir, hashcode))
    # if ret==0:
        # 成功
    return ret


infomat = ["hash", "name", "time", "title"]


def log(dir):
    '''
    输出commit记录
    :param dir: 本地项目的文件夹绝对路径
    '''
    # hash comitter time title
    ret, out = subprocess.getstatusoutput('cd {} && git log --all --encoding=GBK --pretty=format:"%H%n%cn%n%ci%n%s%n"'.format(dir))
    return [dict(zip(infomat, each.split("\n"))) for each in out.split("\n\n")]

def str2base64str(sentence):
    return base64.b64encode(sentence.encode('utf8')).decode('utf8')

def base64str2str(b64str):
    return base64.b64decode(b64str).decode('utf8')

def foldertree(abspath, path_from_projectfolder="", iteractive=False):
    '''
    :param abspath: 被探寻的项目文件夹的绝对路径 D:/projects/myproject1
    :param iteractive: 是否迭代其内的文件
    '''
    # 一个文件夹下的递归结构
    thisfoldername = os.path.split(abspath)[1]
    files = []
    folders = []
    for item in os.listdir(abspath):
        if item.startswith('.'):
            continue
        item_abspath = os.path.join(abspath, item)
        if os.path.isdir(item_abspath):
            if iteractive:
                folders.append(foldertree(
                item_abspath, os.path.join(path_from_projectfolder, item),True))
            else:
                folders.append({
                    'name':item,
                    'rel_path':str2base64str(os.path.join(path_from_projectfolder,item)),
                    'type':'folder'
                    })
        else:
            files.append({
                'name': item, 
                'rel_path': str2base64str(os.path.join(path_from_projectfolder, item)),
                'type':'file'
                })
    return {
        'name': thisfoldername,
        'rel_path':str2base64str(path_from_projectfolder),
        'files': files,
        'folders': folders,
        'type':'folder'
    }

def savebytestodisk(abspath, filecontent):
    if os.path.isfile(abspath):
        with open(abspath,'wb+') as f:
            f.write(filecontent)
        return True
    else:
        return False
        
# Flask部分
app = Flask(__name__)

def checkparam(reqform,*names):
    for name in names:
        if name not in reqform:
            abort(Response("no {} in request form".format(name), status=400))
    return reqform
        

@app.post('/repo/clone')
def repoinfo():
    """
    :param repodir:
    """
    json_data = checkparam(request.form,"repodir")
    repodir = json_data['repodir']
    # clone git仓库
    res = clone(repodir, localstore)
    if res['status'] != 200:
        abort(Response(res['info'], status=400))
    reponame = res['reponame']
    # log
    logs = log(os.path.join(localstore, reponame))
    # foldertree
    thefoldertree = foldertree(os.path.join(localstore, reponame),iteractive=True)
    return jsonify({'reponame': reponame, 'logs': logs, 'foldertree': thefoldertree})

@app.post('/repo/checkout')
def repochk():
    '''
    :param reponame:
    :param hash:
    '''
    json_data = checkparam(request.form,'reponame','hash')
    reponame = json_data['reponame']
    hashcode = json_data['hash']
    # checkout
    res = checkout(os.path.join(localstore, reponame), hashcode)
    if res != 0:
        abort(Response("Checkout Failed",status=400))
    # foldertree
    thefoldertree = foldertree(os.path.join(localstore, reponame),iteractive=True)
    return jsonify({'foldertree': thefoldertree, 'commitid': hashcode})

@app.post('/show/folderplane')
def getfolder():
    """
    :param reponame:
    :param folder_rel_path(base64):
    """
    json_data = checkparam(request.form,"folder_rel_path","reponame")
    folder_rel_path = base64str2str(json_data['folder_rel_path'])
    reponame = json_data['reponame']
    thefolderplane=foldertree(
        os.path.join(localstore,reponame,folder_rel_path),
        path_from_projectfolder=folder_rel_path,
        iteractive=False
    )
    return jsonify({'folderplane':thefolderplane,'upper_folder_rel_path':str2base64str(os.path.split(folder_rel_path)[0])})

@app.post('/show/foldertree')
def getfolderstree():
    """
    :param reponame:
    """
    json_data = checkparam(request.form,"reponame")
    reponame = json_data['reponame']
    thefolderplane=foldertree(
        os.path.join(localstore,reponame),
        path_from_projectfolder="",
        iteractive=True
    )
    return jsonify({'foldertree':thefolderplane})

@app.post('/show/gitlogs')
def getgitlogs():
    """
    :param reponame:
    """
    json_data = checkparam(request.form,"reponame")
    reponame = json_data['reponame']
    # log
    logs = log(os.path.join(localstore, reponame))
    return jsonify({'logs':logs})

@app.post('/get/file')
def getfile():
    """
    :param reponame:
    :param file_rel_path(base64):
    """
    json_data = checkparam(request.form,"file_rel_path","reponame")
    file_path = base64str2str(json_data['file_rel_path'])
    reponame = json_data['reponame']
    file_path = os.path.join(localstore, reponame, file_path)
    # 切割出文件名称
    name = os.path.split(file_path)[-1]
    folder_path = os.path.split(file_path)[0]
    return send_from_directory(path=file_path, directory=folder_path, filename=name, as_attachment=True)

@app.post('/write/file')
def writefile():
    """
    :param reponame:
    :param file_rel_path(base64):
    :param file_content(base64):
    """
    json_data=checkparam(request.form,"reponame","file_rel_path")
    # print(json_data.keys())
    reponame=json_data['reponame']
    file_rel_path=base64str2str(json_data['file_rel_path'])
    # FormData file
    file_content=request.files.get('file_content').read()
    savebytestodisk(os.path.join(localstore,reponame,file_rel_path),file_content)
    return jsonify({"upload":"ok"})


CORS(app, resources=r'/*')
if __name__ == '__main__':
    app.run(host='localhost', port=5000)
