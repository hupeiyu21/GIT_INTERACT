import subprocess
import os
import re
from flask import Flask, jsonify, request, abort, Response, render_template, send_from_directory, current_app
from flask_cors import CORS
from flask_restful import Api
import base64
# Resource
from controller.template import ProductView
from controller.GitRepo.Clone import Clone
from controller.GitRepo.Checkout import Checkout
from controller.GitRepo.Gitlogs import Gitlogs
from controller.File.Folderplane import Folderplane
from controller.File.Foldertree import Foldertree
from controller.File.Getfile import Getfile
from controller.File.Writefile import Writefile

app = Flask(__name__)

localstore=os.path.join(os.path.split(__file__)[0],"storaged")
if not os.path.exists(localstore):
    os.mkdir(localstore)
# relpath: 相对于项目文件夹的相对路径, base64
# abspath：全局路径

app.config['localstore']=localstore
api=Api(app)
# api.add_resource(ProductView, '/show/product', endpoint='product')
api.add_resource(Clone,'/repo/clone',endpoint='clone')
api.add_resource(Checkout,"/repo/checkout",endpoint='checkout')
api.add_resource(Gitlogs,'/show/gitlogs',endpoint='gitlogs')
api.add_resource(Folderplane,'/show/folderplane',endpoint='folderplane')
api.add_resource(Foldertree,'/show/foldertree',endpoint='foldertree')
api.add_resource(Getfile,'/get/file',endpoint='getfile')
api.add_resource(Writefile,'/write/file',endpoint='writefile')

CORS(app, resources=r'/*')
if __name__ == '__main__':
    app.run(host='localhost', port=5000)
