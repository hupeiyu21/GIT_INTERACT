from flask_restful import Resource, reqparse
from flask import current_app,abort,Response,jsonify,send_from_directory,request
import os
from utils.filemanage import foldertree
from utils.base64_turn import base64str2str,str2base64str
from utils.resplit import splitByVersion,needsplit

class Staticfile(Resource):
    
    @staticmethod
    def get():
        # https://blog.csdn.net/qq_27371025/article/details/126721511

        file_path=request.args.get("path")
        
        file_path = os.path.join(current_app.config['localstore'], file_path)
        # 切割出文件名称
        name = os.path.split(file_path)[-1]
        folder_path = os.path.split(file_path)[0]
        
        # print("name",name,"folder",folder_path,"filepath",file_path)
        return send_from_directory(path=file_path, directory=folder_path, filename=name)
        
