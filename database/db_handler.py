import pymysql as sql

conn = sql.connect(host='www.tatine.kr',
				port=3307,
				database='data_analyzer',
				user='jsp',
				password='Gmlqja3520!')

cursor = conn.cursor()

cursor.execute('SELECT * FROM user')
users = cursor.fetchall()

print(users)