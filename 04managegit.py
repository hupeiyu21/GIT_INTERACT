import subprocess
import os
import re
from flask import Flask, jsonify, request, abort, Response, render_template, send_from_directory, current_app
from flask_cors import CORS
from flask_restful import Api
import base64
from redis import StrictRedis
import argparse
# Resource
from controller.template import ProductView
from controller.GitRepo.Clone import Clone
from controller.GitRepo.Checkout import Checkout
from controller.GitRepo.Gitlogs import Gitlogs
from controller.File.Folderplane import Folderplane
from controller.File.Foldertree import Foldertree
from controller.File.Getfile import Getfile
from controller.File.Writefile import Writefile
from controller.File.WriteFileCommit import WritefileCommit
# RedisMQ
from controller.RedisMQ.Push import PushQueue
from controller.RedisMQ.GetQueueRec import GetQueueRec

app = Flask(__name__)

api=Api(app)
# api.add_resource(ProductView, '/show/product', endpoint='product')
api.add_resource(Clone,'/repo/clone',endpoint='clone')
api.add_resource(Checkout,"/repo/checkout",endpoint='checkout')
api.add_resource(Gitlogs,'/show/gitlogs',endpoint='gitlogs')
api.add_resource(Folderplane,'/show/folderplane',endpoint='folderplane')
api.add_resource(Foldertree,'/show/foldertree',endpoint='foldertree')
api.add_resource(Getfile,'/get/file',endpoint='getfile')
api.add_resource(Writefile,'/write/file',endpoint='writefile')
api.add_resource(WritefileCommit,'/commit/file',endpoint='writefilecommit')
# RedisMQ
api.add_resource(PushQueue,'/push/message',endpoint="MQpush")
api.add_resource(GetQueueRec,'/rec/queue',endpoint="MQrec")


CORS(app, resources=r'/*')
if __name__ == '__main__':
    # 命令行参数定义
    paramparser=argparse.ArgumentParser()
    paramparser.add_argument('--redispwd',help='password for Redis')
    # 命令行参数解析获取
    paramopt=paramparser.parse_known_args()[0]
    print("Param of Redis pwd: ",paramopt.redispwd)
    # 
    localstore=os.path.join(os.path.split(__file__)[0],"storaged")
    if not os.path.exists(localstore):
        os.mkdir(localstore)
    app.config['localstore']=localstore
    # Redis连结
    rediscnn=StrictRedis("127.0.0.1",6379,db=2,decode_responses=True)
    app.redis=rediscnn
    # 恢复数据库的脚本的路径
    app.config['DBrecbash_path']="./incre_recover.sh"
    #
    rr,ooutput=subprocess.getstatusoutput('echo %cd%')
    print("we now at {}".format(ooutput))
    app.run(host='localhost', port=5000)
    
