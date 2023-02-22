from flask_restful import Resource, reqparse
from flask import current_app,abort,Response,jsonify 
import os
from utils.gitmanage import clone,log
from utils.filemanage import foldertree
import time
from redis import StrictRedis
import json


class Setnew(Resource):
    
    @staticmethod
    def get():
        """
        :param file_position:
        :param database_name:
        """
        parse = reqparse.RequestParser()
        parse.add_argument('file_position', type=str, help='must need a database file position', required=True, trim=True)
        parse.add_argument('database_name', type=str, help='must need a database name', required=True, trim=True)
        
        args = parse.parse_args()
        file_pos = args['file_position']
        data_name = args['database_name']
        now = int(round(time.time()*1000))
        nowstr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
        # MQ push
        conn=current_app.redis
        conn.set(data_name,json.dumps({"file_position":file_pos,"time":nowstr}))
        return Response("OK",status=200)