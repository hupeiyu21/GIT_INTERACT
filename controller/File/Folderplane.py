from flask_restful import Resource, reqparse
from flask import current_app,abort,Response,jsonify
from utils.base64_turn import base64str2str,str2base64str
from utils.filemanage import foldertree
import os

class Folderplane(Resource):
    
    @staticmethod
    def post():
        # https://blog.csdn.net/qq_27371025/article/details/126721511
        parse = reqparse.RequestParser()
        parse.add_argument('reponame', type=str, help='need reponame', required=True, trim=True, location='form')
        parse.add_argument('folder_rel_path',type=str,help='need rel_path',required=True,trim=True,location='form')
        args = parse.parse_args()
        folder_rel_path = base64str2str(args['folder_rel_path'])
        reponame = args['reponame']
        thefolderplane=foldertree(
            os.path.join(current_app.config['localstore'],reponame,folder_rel_path),
            path_from_projectfolder=folder_rel_path,
            iteractive=False
        )
        return jsonify({'folderplane':thefolderplane,'upper_folder_rel_path':str2base64str(os.path.split(folder_rel_path)[0])})