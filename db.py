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

	print "DB connection closed: {}".format(not connected)


# ---------- user management ----------

def login(username, password):

	query = "SELECT * FROM user WHERE username = %s AND password = %s"
	response = cursor.execute(query, (username, password))
	if  not response:
		return 0
	else:
		query = "SELECT usertype FROM user WHERE username = %s AND password = %s"
		response = cursor.execute(query, (username, password))
		response = cursor.fetchone()
		if response[0] == 'City Scientist':
			return 1
		elif response[0] == 'City Official':
			return 2
		elif response[0] == 'Admin':
			return 3

def register(username, email, password, usertype):
	try:
		query = "INSERT INTO user(username, email, password, usertype) VALUES(%s, %s, %s, %s)"
		response = cursor.execute(query, (username, email, password, usertype))
		database.commit()
		return True
	except:
		return False


# ---------- adding new data ----------

def addNewPOILocation(locationName, city, state, zipCode):
	return None


def addNewDataPoint(poiLocation, date_time, dataType, value):
	try:
		query = "INSERT into dataPoint(poi_location_name, date_time, data_type, data_value, accepted) VALUES(%s, %s, %s, %s, 0)"
		response = cursor.execute(query, (poiLocation, date_time, dataType, value))
		database.commit()
		print response
		return True
	except:
		print "error"
		return False
		










