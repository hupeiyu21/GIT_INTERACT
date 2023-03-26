from flask_restful import Resource, reqparse
from flask import current_app,abort,Response,jsonify
import os
from utils.gitmanage import log,nowcommit

class Gitlogs(Resource):
    
    @staticmethod
    def post():
        # https://blog.csdn.net/qq_27371025/article/details/126721511
        parse = reqparse.RequestParser()
        parse.add_argument('reponame', type=str, help='need reponame', required=True, trim=True, location='form')
        args = parse.parse_args()
        
        reponame = args['reponame']
        # log
        logs = log(os.path.join(current_app.config['localstore'], reponame))
        nowcommitid=nowcommit(os.path.join(current_app.config['localstore'], reponame))
        return jsonify({'logs':logs,'commitid':nowcommitid})
        