import subprocess

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

def commit(commitname,dir):
    ret, out = subprocess.getstatusoutput(
        'cd {} && git add . && git commit -m {}'.format(dir, commitname))
    if ret==0:
        return True
    return False

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