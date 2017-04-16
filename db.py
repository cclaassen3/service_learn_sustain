import MySQLdb


connected = False
database = None
cursor = None

def setUp():
	global db
	global cursor
	if not connected:
		try:
			db = MySQLdb.connect(host="academic-mysql.cc.gatech.edu", user="cs4400_Group_20", passwd="3lZwg9Kk", db="cs4400_Group_20")
			cursor = db.cursor()
			connected = True
		except Exception as e:
			connected = False

def end():
	global connected
	if connected:
		database.close()
		connected = False


def register(username, email, password, usertype):
	cursor.execute("INSERT INTO user(username, email, password, usertype) VALUES(%s, %s, %s, %s)", insertedUser, insertedEmail, insertedPass, insertedType)
	database.commit()