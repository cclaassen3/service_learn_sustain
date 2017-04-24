import db_config
import MySQLdb

# ---------- variable setup ----------

connected = False
database = None
cursor = None

data_point_filter = None
poi_report_filter = None


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

	query = "SELECT * FROM user WHERE username=%s AND password=%s"
	response = cursor.execute(query, (username, password))
	if not response:
		return None
	else:
		query = "SELECT usertype FROM user WHERE username=%s AND password=%s"
		cursor.execute(query, (username, password))
		response = cursor.fetchone()
		if response[0] == 'Admin': return 'admin'
		elif response[0] == 'City Scientist': return 'cityScientist'
		elif response[0] == 'City Official':

			#check to make sure city official account has been approved
			query = "SELECT * FROM cityOfficial WHERE username=%s AND approved=True"
			response = cursor.execute(query, (username,))
			if not response: return 'unapprovedCO'
			return 'cityOfficial'

def register(username, email, password, usertype):
	try:
		query = "INSERT INTO user(username, email, password, usertype) VALUES(%s, %s, %s, %s)"
		response = cursor.execute(query, (username, email, password, usertype))
		database.commit()
		return True
	except:
		return False


# ---------- data insertion ----------

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
		query = "INSERT into dataPoint(poi_location_name, date_time, data_type, data_value, accepted) VALUES(%s, %s, %s, %s, NULL)"
		response = cursor.execute(query, (poiLocation, date_time, dataType, value))
		print "response:", response
		database.commit()
		return True
	except:
		return False

def addCityOfficial(username, city, state, title):
	try:
		query = "INSERT INTO cityOfficial(username, city, state, title) VALUES(%s, %s, %s, %s)"
		response = cursor.execute(query, (username, city, state, title))
		database.commit()
		return True
	except:
		print "Error adding city official to the DB"

def flagPOI(poiLocation):
	query = "UPDATE POI SET flag = 1, date_flagged=sysdate WHERE location_name = %s"
	response = cursor.execute(query, (poiLocation,))
	database.commit()
	return cursor.fetchall()


# ---------- data retrieval ----------
	
def retrieveFilteredDataPoints(dictionary):
		#query = "SELECT * FROM poi WHERE location_name=%s AND city =%s AND state=%s AND flag=%s AND date_flagged > %s AND date_flagged < %s"
		query = "SELECT * FROM poi"
		# if dictionary:
		# 	query += " WHERE "
		# 	if "location_name" in dictionary.keys():
		# 		query += "location_name={}".format(dictionary["location_name"])
		# 	if "City" in dictionary.keys():
		# 		query += "City={}".format(dictionary["City"])
		# 	if "State" in dictionary.keys():
		# 		query += "State={}".format(dictionary["State"])

		cursor.execute(query)
		database.commit()
		return cursor.fetchall()

def retrieveDataForLocation(poiLocation): 
	query = "SELECT data_type, data_value, date_time FROM dataPoint WHERE poi_location_name = %s"
	cursor.execute(query, (poiLocation,))
	database.commit()
	return cursor.fetchall()

def retrieveDataForPOIDetails(poiLocation, datetime1, datetime2, datapoint1, datapoint2, datatype): 
	query = "SELECT data_type, data_value, date_time FROM dataPoint WHERE poi_location_name = %s AND date_time >= %s AND date_time <= %s AND data_value >= %s AND data_value <= %s AND data_type = %s"
	cursor.execute(query, (poiLocation, datetime1, datetime2, datapoint1, datapoint2, datatype))
	database.commit()
	return cursor.fetchall()

def existsUsername(username):
	query = "SELECT username FROM user WHERE username=%s"
	cursor.execute(query, (username,))
	return len(cursor.fetchall()) > 0

def existsEmail(email):
	query = "SELECT email FROM user WHERE email=%s"
	cursor.execute(query, (email,))
	return len(cursor.fetchall()) > 0

def retrieveDataPoints():
	if data_point_filter: return filteredDataPoints(data_point_filter)
	query = "SELECT poi_location_name, data_type, data_value, date_time FROM dataPoint WHERE accepted is NULL"
	cursor.execute(query)
	return cursor.fetchall()

def filteredDataPoints(filter_specs):
	#set ascending / descending
	ascdesc = 'asc'
	if filter_specs[0] == 'desc': ascdesc = 'desc'

	#set column to filter by
	column = 'poi_location_name'
	if filter_specs[1] == 'data':
		if filter_specs[2] == 'type': column = 'data_type'
		elif filter_specs[2] == 'value': column = 'data_value'
	elif filter_specs[1] == 'date': column = 'date_time'

	#retrieve data points
	query = "SELECT poi_location_name, data_type, data_value, date_time FROM dataPoint WHERE accepted is NULL order by {} {}".format(column, ascdesc)
	cursor.execute(query)
	return cursor.fetchall()

def retrieveCityOfficials():
	query = "SELECT username, email, City, State, title FROM cityOfficial NATURAL JOIN user WHERE approved is NULL"
	cursor.execute(query)
	return cursor.fetchall()

def retrievePOILocations():
	query = "SELECT location_name FROM poi"
	cursor.execute(query)
	return cursor.fetchall()

def retrieveDataTypes():
	query = "SELECT * FROM dataType"
	cursor.execute(query)
	return cursor.fetchall()

def retrieveCities():
	query = "SELECT DISTINCT city FROM cityState"
	cursor.execute(query)
	return cursor.fetchall()

def retrieveStates():
	query = "SELECT DISTINCT state FROM cityState"
	cursor.execute(query)
	return cursor.fetchall()

def existsCityState(city, state):
	query = "SELECT * FROM cityState WHERE city=%s AND state=%s"
	cursor.execute(query, (city, state))
	return len(cursor.fetchall()) > 0

def retrievePOIReportRows():
	if poi_report_filter: return filteredPOIReportRows(poi_report_filter)
	query = "SELECT dp1.poi_location_name, poi.City, poi.State, MIN( dp2.data_value ) AS Mold_Min, AVG( dp2.data_value ) AS Mold_Avg, MAX( dp2.data_value ) AS Mold_Max, MIN( dp3.data_value ) AS AQ_Min, AVG( dp3.data_value ) AS AQ_Avg, MAX( dp3.data_value ) AS AQ_Max, COUNT( DISTINCT ( dp1.date_time ) ) AS num_of_data_points, poi.flag FROM dataPoint dp1 LEFT JOIN dataPoint dp2 ON dp1.poi_location_name = dp2.poi_location_name AND dp2.data_type = 'Mold' LEFT JOIN dataPoint dp3 ON dp1.poi_location_name = dp3.poi_location_name AND dp3.data_type = 'Air Quality' LEFT JOIN poi ON dp1.poi_location_name = poi.location_name GROUP BY poi_location_name"
	cursor.execute(query)
	return cursor.fetchall()

def filteredPOIReportRows(filter_specs):
	query = "SELECT dp1.poi_location_name, poi.City, poi.State, MIN( dp2.data_value ) AS Mold_Min, AVG( dp2.data_value ) AS Mold_Avg, MAX( dp2.data_value ) AS Mold_Max, MIN( dp3.data_value ) AS AQ_Min, AVG( dp3.data_value ) AS AQ_Avg, MAX( dp3.data_value ) AS AQ_Max, COUNT( DISTINCT ( dp1.date_time ) ) AS num_of_data_points, poi.flag FROM dataPoint dp1 LEFT JOIN dataPoint dp2 ON dp1.poi_location_name = dp2.poi_location_name AND dp2.data_type = 'Mold' LEFT JOIN dataPoint dp3 ON dp1.poi_location_name = dp3.poi_location_name AND dp3.data_type = 'Air Quality' LEFT JOIN poi ON dp1.poi_location_name = poi.location_name GROUP BY poi_location_name"

	#set ascending / descending
	ascdesc = 'asc'
	if filter_specs[0] == 'desc': ascdesc = 'desc'

	#determine what column / statistic to filter by
	if filter_specs[1] == 'mold':
		if filter_specs[2] == 'min': 
			query += " ORDER BY Mold_Min {}".format(ascdesc)
		elif filter_specs[2] == 'avg': 
			query += " ORDER BY Mold_Avg {}".format(ascdesc)
		else: 
			query += " ORDER BY Mold_Max {}".format(ascdesc)

	elif filter_specs[1] == 'AQ': 
		if filter_specs[2] == 'min': 
			query += " ORDER BY AQ_Min {}".format(ascdesc)
		elif filter_specs[2] == 'avg': 
			query += " ORDER BY AQ_Avg {}".format(ascdesc)
		else: 
			query += " ORDER BY AQ_Max {}".format(ascdesc)

	elif filter_specs[1] == 'num':
		query += " ORDER BY num_of_data_points {}".format(ascdesc)

	elif filter_specs[1] == 'flagged':
		query += " ORDER BY poi.flag {}".format(ascdesc)

	#retrieve data points
	cursor.execute(query)
	return cursor.fetchall()


# ---------- data modification ----------

def acceptDataPoint(poi_location, date_time):
	try:
		query = "UPDATE dataPoint SET accepted=True WHERE poi_location_name=%s and date_time=%s"
		cursor.execute(query, (poi_location, date_time))
		database.commit()
	except:
		print "error accepting data point: {} {}".format(poi_location, date_time)

def rejectDataPoint(poi_location, date_time):
	try:
		query = "UPDATE dataPoint SET accepted=0 WHERE poi_location_name=%s and date_time=%s"
		cursor.execute(query, (poi_location, date_time))
		database.commit()
	except:
		print "error rejecting data point: {} {}".format(poi_location, date_time)

def acceptCityOfficial(username):
	try:
		query = "UPDATE cityOfficial SET approved=True WHERE username=%s"
		cursor.execute(query, (username,))
		database.commit()
	except:
		print "error accepting city official: {}".format(username)

def rejectCityOfficial(username):
	try:
		query = "UPDATE cityOfficial SET approved=False WHERE username=%s"
		cursor.execute(query, (username,))
		database.commit()
	except:
		print "error rejecting city official: {}".format(username)













