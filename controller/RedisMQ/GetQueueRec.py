from flask_restful import Resource, reqparse
from flask import current_app,abort,Response,jsonify 
import os
from utils.gitmanage import clone,log
from utils.filemanage import foldertree,checkfiles_exist
import time
from redis import StrictRedis
import subprocess
import argparse
import json

from utils.rediscontrol import getMQList

class GetQueueRec(Resource):
    
    @staticmethod
    def get():
        """
        :param new_db_name:
        :param old_db_name
        """
        parse = reqparse.RequestParser()
        parse.add_argument('old_db_name', type=str, help='must need a database name', required=True, trim=True)
        
        args = parse.parse_args()
        old_db_name = args['old_db_name']
        # MQ push (streamid,{k:v,k:v})
        conn=current_app.redis
        # 文件列表
        returnredisstr=" ".join([each[1]['file_position'] for each in getMQList(conn,old_db_name)])

        # 检查是否存在
        checkres=checkfiles_exist(returnredisstr.split(" "))
        if(not checkres['res']):
            return Response(json.dumps({'res':'error','msg':'such backup files {} do not exist'.format(",".join(checkres['filelist']))}),status=400)
        ret, out = subprocess.getstatusoutput('bash {} -uroot -ppassword -P3306 -hIP -d {} -f "{}"'.format(current_app.config['DBrecbash_path'],old_db_name,returnredisstr))
        print("Run recursive revocery, code={}, out={}".format(ret,out))
        return {'res':'success','msg':returnredisstr}