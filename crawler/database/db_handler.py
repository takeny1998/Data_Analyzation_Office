import pymysql as sql
import configparser
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

	def insert_crawling_data(self, type, clean_words):
		now = time.strftime('%Y-%m-%d')
		hours = int(time.strftime('%H'))
		times = int(hours / 3)

		sql = '''
			INSERT INTO crawling_data
			VALUES(null, %s, %s, %s, %s)'''

		self.cursor.execute(sql, (now, times, type, clean_words))
		self.conn.commit()

	def close(self):
		self.conn.close()
	