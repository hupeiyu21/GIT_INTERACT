from flask_restful import Resource, reqparse
from flask import current_app,abort,Response,jsonify 
import os
from utils.gitmanage import clone,log
from utils.filemanage import foldertree

class Clone(Resource):
    
    @staticmethod
    def post():
        """
        :param repodir:
        """
        parse = reqparse.RequestParser()
        parse.add_argument('repodir', type=str, help='must need a repo url', required=True, trim=True, location='form')
        args = parse.parse_args()
        repodir = args['repodir']
        # clone git仓库
        res = clone(repodir, current_app.config['localstore'])
        if res['status'] != 200:
            abort(Response(res['info'], status=400))
        reponame = res['reponame']
        # log
        logs = log(os.path.join(current_app.config['localstore'], reponame))
        # foldertree
        thefoldertree = foldertree(os.path.join(current_app.config['localstore'], reponame),iteractive=True)
        return jsonify({'reponame': reponame, 'logs': logs, 'foldertree': thefoldertree})