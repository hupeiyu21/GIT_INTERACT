from flask_restful import Resource, reqparse
from flask import current_app,abort,Response,jsonify 
import os
from utils.gitmanage import clone,log
from utils.filemanage import foldertree
import time
from redis import StrictRedis
import subprocess
import argparse

from utils.rediscontrol import getMQList

class GetQueueRec(Resource):
    
    @staticmethod
    def get():
        """
        :param new_db_name:
        :param old_db_name
        """
        parse = reqparse.RequestParser()
        parse.add_argument('new_db_name', type=str, help='must need new database name', required=True, trim=True)
        parse.add_argument('old_db_name', type=str, help='must need a database name', required=True, trim=True)
        
        args = parse.parse_args()
        new_db_name = args['new_db_name']
        old_db_name = args['old_db_name']
        # MQ push
        conn=current_app.redis
        # (streamid,{k:v,k:v})
        returnstr=" ".join([each[1]['file_position'] for each in getMQList(conn,old_db_name)])
        ret, out = subprocess.getstatusoutput('bash {} -uroot -ppassword -P3306 -hIP -d {} -f "{}"'.format(current_app.config['DBrecbash_path'],new_db_name,returnstr))
        print("Run revocery, code={}, out={}".format(ret,out))
        return Response(returnstr,status=200)