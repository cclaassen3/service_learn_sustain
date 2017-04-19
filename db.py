import db_config
import MySQLdb

# ---------- variable setup ----------

connected = False
database = None
cursor = None

# ---------- database connection functions ----------

def setUp():
	global database
	global cursor
	global connected

	if not connected:
		try:
			database = MySQLdb.connect(host=db_config.host, user=db_config.user, passwd=db_config.passwd, db=db_config.db)
			cursor = database.cursor()
			connected = True
		except Exception as e:
			connected = False

		print "DB connection established: {}".format(connected)

def end():
	global connected
	if connected:
		database.close()
		connected = False


# ---------- data retrieval ----------

def login(username, password):
	query = "SELECT * FROM user WHERE username = %s AND password = %s"
	response = cursor.execute(query, (username, password))
	if response == 0:
		return 0
	else: 
		query = "SELECT usertype FROM user WHERE username = %s AND password = %s"
		response = cursor.execute(query, (username, password))
		response = cursor.fetchone()
		if response[0] == 'City Scientist':
			return 1
		else: 
			return 2


# ---------- data updates -----------

def register(username, email, password, usertype):
	query = "INSERT INTO user(username, email, password, usertype) VALUES(%s, %s, %s, %s)"
	response=cursor.execute(query, (username, email, password, usertype))
	database.commit()