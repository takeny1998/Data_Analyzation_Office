import pymysql as sql
import configparser
import json
import time


class DBHandler:
	
	def __init__(self):
		# parse 'config.ini' file automatically
		# please find 'config.ini' file or create it and place it in 'root' folder
		# and enter your mysql or mariadb connection information
		parser = configparser.ConfigParser()
		parser.read('config.ini')

		DB_props = parser["DATABASE"]
		DB_HOST = DB_props['HOST']
		DB_PORT = DB_props.getint('PORT')
		DB_NAME = DB_props['NAME']
		DB_USER = DB_props['USER']
		DB_PW = DB_props['PW']

		self.conn = sql.connect(
						host=DB_HOST,
						port=DB_PORT,
						database=DB_NAME,
						user=DB_USER,
						password=DB_PW)
	
		self.cursor = self.conn.cursor()

	def insert_crawling_data(self, type, top_10, top_30, top_200):
		now = time.strftime('%Y-%m-%d %H:%M:%S')
		sql = '''
			INSERT INTO data
			VALUES(null, %s, %s, %s, %s, %s)'''

		self.cursor.execute(sql, (now, type, top_10, top_30, top_200))
		self.conn.commit()

	def close(self):
		self.conn.close()
	
db = DBHandler()