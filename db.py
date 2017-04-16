import MySQLdb


connected = False
database = None
cursor = None

def setUp():
	global database
	global cursor
	global connected

	if not connected:
		try:
			database = MySQLdb.connect(host="academic-mysql.cc.gatech.edu", user="cs4400_Group_20", passwd="3lZwg9Kk", db="cs4400_Group_20")
			cursor = database.cursor()
			connected = True
		except Exception as e:
			connected = False

def end():
	global connected
	if connected:
		database.close()
		connected = False


def register(username, email, password, usertype):
	query = "INSERT INTO user(username, email, password, usertype) VALUES(%s, %s, %s, %s)"
	response=cursor.execute(query, (username, email, password, usertype))
	database.commit()