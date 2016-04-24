import mysql.connector
import json

def parsedbconf():
    global dbconffile
    with open(dbconffile) as data_file:
        data = json.load(data_file)
        return data

def getdbconnection():
    global cnx
    data = parsedbconf()
    cnx = mysql.connector.connect(user=data["db"][0]["user"],
                                  password=data["db"][0]["password"],
                                  host=data["db"][0]["host"],
                                  database=data["db"][0]["database"])
    return cnx

def query_clean_daily_access():
    cnx = getdbconnection()
    cursor = cnx.cursor()
    query = "TRUNCATE `ist176550`.`DAILY_REGISTER`;"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

global dbconffile
dbconffile = "/home/pi/sirsproject/mysqldoor/Door/dbdata.json" 
query_clean_daily_access()
