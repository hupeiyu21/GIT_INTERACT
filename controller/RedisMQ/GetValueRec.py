from flask_restful import Resource, reqparse
from flask import current_app,abort,Response,jsonify 
import os
from utils.gitmanage import clone,log
from utils.filemanage import checkfiles_exist
import time
from redis import StrictRedis
import subprocess
import argparse
import json

from utils.rediscontrol import getValue

class GetValueRec(Resource):
    
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
        returnredisstr=getValue(conn,old_db_name)
        if(not returnredisstr):
            return Response(json.dumps({'res':'invalid','msg':'no backup databse name'}),status=400)
        returndict=json.loads(returnredisstr)
        
        # 检查是否存在
        checkres=checkfiles_exist([returndict["file_position"]])
        if(not checkres['res']):
            return abort(jsonify({'res':'error','msg':'such backup files {} do not exist'.format(",".join(checkres['filelist']))}))
        ret, out = subprocess.getstatusoutput('bash {} -uroot -ppassword -P3306 -hIP -d {} -f "{}"'.format(current_app.config['DBfullbash_path'],old_db_name,returndict["file_position"]))
        print("Run full revocery, code={}, out={}".format(ret,out))
        return {'res':'success','msg':returndict}