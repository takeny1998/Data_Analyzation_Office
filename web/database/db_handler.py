from distutils.command.clean import clean
import pymysql
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
		self.__conn = pymysql.connect(
						host=DB_HOST,
						port=DB_PORT,
						database=DB_NAME,
						user=DB_USER,
						password=DB_PW)
	

	def get_crawling_data(self, date, times):
		result = {}

		dict_cursor = self.__conn.cursor(pymysql.cursors.DictCursor)
		sql = '''
			SELECT * FROM crawling_data
			WHERE date=%s AND times=%s'''

		dict_cursor.execute(sql, (date, times))
		sql_rs = dict_cursor.fetchall()

		for row in sql_rs:
			arr = []
			clean_words = json.loads(row['clean_words'])

			for key, value in clean_words.items():
				arr.append({
					'x': key,
					'value': value
				})
			result[row['type']] = arr
		return result

	def close(self):
		self.__conn.close()
	
db = DBHandler()