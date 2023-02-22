from utils.base64_turn import str2base64str,base64str2str
import os

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
    
def checkfiles_exist(filepathlist):
    """
    check whether a range of files are in disk
    """
    donothave=[]
    for file in filepathlist:
        if(not os.path.exists(file)):
            donothave.append(file)
    if donothave:
        return {'res':False,'filelist':donothave}
    return {'res':True}