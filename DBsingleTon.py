import os,sys
import MySQLdb
import mysql.connector
sys.path.insert(1,os.path.join(os.path.dirname(__file__), '..', 'lib'))
from config import Config

class DBsingleTon:	
	def __init__(self):
		self.db_conns = {}
		self.DBconfig = Config.get()['db_config']
		
	@staticmethod
	def get_connection_obj(self,host,user,passwd,db_name):
		pid = os.getpid()
		if not pid in self.db_conns:
			self.db_conns[pid] = mysql.connector.connect(
				user=    user,
				passwd=  passwd if passwd is not None else '',
				db=      db_name,
				host=    host)
		return self.db_conns[pid]

	def db_conn(self):
		return self.get_connection_obj(self,
			self.DBconfig['host'],
			self.DBconfig['user'],
			self.DBconfig['passwd'],
			self.DBconfig['db'])
