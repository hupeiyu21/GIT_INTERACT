from flask_restful import Resource, reqparse
from flask import current_app,abort,Response,jsonify
import os
from utils.filemanage import foldertree

class Foldertree(Resource):
    
    @staticmethod
    def post():
        # https://blog.csdn.net/qq_27371025/article/details/126721511
        parse = reqparse.RequestParser()
        parse.add_argument('reponame', type=str, help='need reponame', required=True, trim=True, location='form')
        args = parse.parse_args()
        reponame = args['reponame']
        thefolderplane=foldertree(
            os.path.join(current_app.config['localstore'],reponame),
            path_from_projectfolder="",
            iteractive=True
        )
        return {'foldertree':thefolderplane}
        
