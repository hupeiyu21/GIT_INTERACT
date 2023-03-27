import re

pattern=re.compile(r'<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> [0-9a-z]+?\n',flags=re.DOTALL)

# 将冲突文件分成两个版本的字符串
def splitByVersion(filepath):
    with open(filepath,"r",encoding="utf8") as f:
        fcontent=f.read()
        # reres=pattern.findall(fcontent)
        # print(reres)
        res={"local":re.sub(pattern,r'\1',fcontent),"remote":re.sub(pattern,r'\2',fcontent)}
        return res
    
# 检测文件是否是冲突文件
def needsplit(filepath):
    with open(filepath,"r",encoding="utf8") as f:
        fcontent=f.read()
        reres=pattern.search(fcontent)
        return reres
    