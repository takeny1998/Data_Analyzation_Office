from distutils.command.clean import clean
import pymysql
import configparser
import json
import time
from itertools import islice

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
		self.__conn = pymysql.connect(
						host=DB_HOST,
						port=DB_PORT,
						database=DB_NAME,
						user=DB_USER,
						password=DB_PW)
	

	def get_crawling_data(self, date, times, type):
		dict_cursor = self.__conn.cursor(pymysql.cursors.DictCursor)
		sql = '''
			SELECT * FROM crawling_data
			WHERE date=%s AND times=%s AND type=%s'''

		dict_cursor.execute(sql, (date, times, type))
		sql_rs = dict_cursor.fetchone()

		clean_words = json.loads(sql_rs['clean_words'])
		return clean_words


	def close(self):
		self.__conn.close()
	
db = DBHandler()