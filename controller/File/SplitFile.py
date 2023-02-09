from flask_restful import Resource, reqparse
from flask import current_app,abort,Response,jsonify
import os
from utils.base64_turn import base64str2str
from utils.resplit import splitByVersion

class SplitFile(Resource):
    
    @staticmethod
    def post():
        parse = reqparse.RequestParser()
        parse.add_argument('reponame', type=str, help='need reponame', required=True, trim=True, location='form')
        parse.add_argument('file_rel_path', type=str, help='need file_rel_path', required=True, trim=True, location='form')        
        args = parse.parse_args()
        
        reponame = args['reponame']
        file_path=base64str2str(args['file_rel_path'])
        
        file_path = os.path.join(current_app.config['localstore'], reponame, file_path)
        
        return jsonify(splitByVersion(file_path))
        
