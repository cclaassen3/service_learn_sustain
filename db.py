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
	try:
		query = "INSERT into poi(location_name, zip_code, city, state, flag) VALUES(%s, %s, %s, %s, 0)"
		response = cursor.execute(query, (locationName, zipCode, city, state))
		print "response:", response
		database.commit()
		return True
	except:
		return False

def addNewDataPoint(poiLocation, date_time, dataType, value):
	try:
		query = "INSERT into dataPoint(poi_location_name, date_time, data_type, data_value, accepted) VALUES(%s, %s, %s, %s, 0)"
		response = cursor.execute(query, (poiLocation, date_time, dataType, value))
		print "response:", response
		database.commit()
		return True
	except:
		return False
		


# ---------- fetch data -----------

def retrieveDataPoints():
	query = "SELECT * FROM dataPoint WHERE accepted=0"
	cursor.execute(query)
	database.commit()
	return cursor.fetchall()

def retrievePOILocations():
	query = "SELECT location_name FROM poi"
	cursor.execute(query)
	database.commit()
	return cursor.fetchall()

def retrieveDataTypes():
	query = "SELECT * FROM dataType"
	cursor.execute(query)
	database.commit()
	return cursor.fetchall()

def retrieveCities():
	query = "SELECT city FROM cityState"
	cursor.execute(query)
	database.commit()
	return cursor.fetchall()

def retrieveStates():
	query = "SELECT state FROM cityState"
	cursor.execute(query)
	database.commit()
	return cursor.fetchall()

def existsCityState(city, state):
	query = "SELECT * FROM cityState WHERE city=%s AND state=%s"
	cursor.execute(query, (city, state))
	database.commit()
	return len(cursor.fetchall()) > 0











