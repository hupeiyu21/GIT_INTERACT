from flask_restful import Resource, reqparse
from flask import current_app,abort,Response,jsonify
import os
from utils.filemanage import foldertree

class ProductView(Resource):
    
    @staticmethod
    def post():
        # https://blog.csdn.net/qq_27371025/article/details/126721511
        parse = reqparse.RequestParser()
        parse.add_argument('reponame', type=str, help='need reponame', required=True, trim=True, location='form')
        args = parse.parse_args()
        
