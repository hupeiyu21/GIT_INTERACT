from flask_restful import Resource, reqparse
from flask import current_app,abort,Response,jsonify
import os
from utils.filemanage import foldertree
from utils.gitmanage import nowcommit
from utils.gitmanage import pull,diff

class Difflist(Resource):
    
    @staticmethod
    def post():
        # https://blog.csdn.net/qq_27371025/article/details/126721511
        parse = reqparse.RequestParser()
        parse.add_argument('reponame', type=str, help='need reponame', required=True, trim=True, location='form')

        args = parse.parse_args()
        
        reponame=args["reponame"]
        repodir=os.path.join(current_app.config['localstore'],reponame)
        # 显示冲突
        return {'msg':"existed files conflict",'files':diff(repodir)},200
        
