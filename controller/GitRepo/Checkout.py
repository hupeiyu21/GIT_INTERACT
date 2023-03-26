from flask_restful import Resource, reqparse
from flask import current_app,abort,Response,jsonify
import os
from utils.gitmanage import checkout
from utils.filemanage import foldertree

class Checkout(Resource):
    @staticmethod
    def post():
        # https://blog.csdn.net/qq_27371025/article/details/126721511
        parse = reqparse.RequestParser()
        parse.add_argument('reponame', type=str, help='need reponame', required=True, trim=True, location='form')
        parse.add_argument('hash',type=str,help="need hash",required=True,trim=True,location='form')
        args = parse.parse_args()
        reponame = args['reponame']
        hashcode = args['hash']
        # checkout
        res = checkout(os.path.join(current_app.config['localstore'], reponame), hashcode)
        if res != 0:
            return {"msg":"Checkout Failed"},400
        # foldertree
        thefoldertree = foldertree(os.path.join(current_app.config['localstore'], reponame),iteractive=True)
        return {"msg":"success checkout",'foldertree': thefoldertree, 'commitid': hashcode}