import pymysql as sql
import configparser

class DbHandler:
	
	def __init__(self):
		# parse 'config.ini' file automatically
		# please find 'config.ini' file or create it and place it in 'root' folder
		# and enter your mysql or mariadb connection information
		parser = configparser.ConfigParser()
		parser.read('config.ini')

		db_props = parser["DATABASE"]
		DB_HOST = db_props['HOST']
		DB_PORT = db_props.getint('PORT')
		DB_NAME = db_props['NAME']
		DB_USER = db_props['USER']
		DB_PW = db_props['PW']

		conn = sql.connect(
						host=DB_HOST,
						port=DB_PORT,
						database=DB_NAME,
						user=DB_USER,
						password=DB_PW)
	
		self.cursor = conn.cursor()

	
	
db = DbHandler()