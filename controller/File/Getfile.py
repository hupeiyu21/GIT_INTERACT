from flask_restful import Resource, reqparse
from flask import current_app,abort,Response,jsonify,send_from_directory
import os
from utils.filemanage import foldertree
from utils.base64_turn import base64str2str,str2base64str
from utils.resplit import splitByVersion,needsplit

class Getfile(Resource):
    
    @staticmethod
    def post():
        # https://blog.csdn.net/qq_27371025/article/details/126721511
        parse = reqparse.RequestParser()
        parse.add_argument('file_rel_path', type=str, help='need file_rel_path', required=True, trim=True, location='form')
        parse.add_argument('reponame', type=str, help='need reponame', required=True, trim=True, location='form')
        
        args = parse.parse_args()
        file_path = base64str2str(args['file_rel_path'])
        reponame = args['reponame']
        file_path = os.path.join(current_app.config['localstore'], reponame, file_path)
        # 切割出文件名称
        name = os.path.split(file_path)[-1]
        folder_path = os.path.split(file_path)[0]
        # 打印下是否需要切割
        # print(needsplit(file_path))
        if(not needsplit(file_path)):
            # 不需要
            return send_from_directory(path=file_path, directory=folder_path, filename=name, as_attachment=True)
        else:
            return splitByVersion(file_path),400
        
