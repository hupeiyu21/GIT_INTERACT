from flask_restful import Resource, reqparse
from flask import current_app,abort,Response,jsonify
import os
from utils.gitmanage import commit

class CommitAll(Resource):
    
    @staticmethod
    def post():
        # https://blog.csdn.net/qq_27371025/article/details/126721511
        parse = reqparse.RequestParser()
        parse.add_argument('reponame', type=str, help='need reponame', required=True, trim=True, location='form')
        parse.add_argument('message', type=str, help='need message', required=True, trim=True, location='form')
        args = parse.parse_args()
        
        reponame=args["reponame"]
        commitmsg=args["message"]
        if(commit(commitmsg,os.path.join(current_app.config['localstore'],reponame))):
            return {"msg":"success commit"}
        return {"msg":"error when commit or nothing to commit"},400
        
