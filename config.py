import MySQLdb
import mysql.connector
import MySQLdb.cursors
import os
import yaml

class Config():
    @staticmethod
    def get():
        config_file = os.path.join(os.path.dirname(__file__), "..", "conf", "config.yml")
        with open("confi.yaml","r") as outfile:
            return yaml.load(outfile)

    #conn = mysql.connector.connect(user = cfg['user'],passwd= cfg['passwd'],db=cfg['db'],host= cfg['host'])
    #return conn