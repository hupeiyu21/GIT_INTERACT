from flask_restful import Resource, reqparse
from flask import current_app,abort,Response,jsonify
from werkzeug.datastructures import FileStorage
import os
from utils.filemanage import foldertree,savebytestodisk
from utils.gitmanage import commit
from utils.base64_turn import base64str2str

class WritefileCommit(Resource):
    
    @staticmethod
    def post():
        # https://blog.csdn.net/qq_27371025/article/details/126721511
        parse = reqparse.RequestParser()
        parse.add_argument('reponame', type=str, help='need reponame', required=True, trim=True, location='form')
        parse.add_argument('file_rel_path', type=str, help='need file_rel_path', required=True, trim=True, location='form')
        parse.add_argument('commit_message',type=str,required=False,location="form")
        parse.add_argument('file_content',type=FileStorage,required=True,location="files")
        
        args = parse.parse_args()
        reponame=args['reponame']
        commitmsg=args['commit_message']
        file_rel_path=base64str2str(args['file_rel_path'])
        # FormData file
        file_content=args['file_content'].read()
        savebytestodisk(os.path.join(current_app.config['localstore'],reponame,file_rel_path),file_content)
        if(commit(commitmsg,os.path.join(current_app.config['localstore'],reponame))):
            return {"msg":"Successful save and commit"}
        else:
            return {"msg":"Successful save, error commit"},400
