import mysql.connector
import json
from pprint import pprint

dbconffile = 'Door/dbdata.json'
#dbconffile = 'dbdata.json'



def db_parsedbconf():
    global dbconffile
    with open(dbconffile) as data_file:
        data = json.load(data_file)
        return data


def db_getdbconnection():
    global cnx
    data = db_parsedbconf()
    cnx = mysql.connector.connect(user=data["db"][0]["user"],
                                  password=data["db"][0]["password"],
                                  host=data["db"][0]["host"],
                                  database=data["db"][0]["database"])
    return cnx
    # cnx.close()


def db_query(query):
    cnx = db_getdbconnection()
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.close()
    return cursor

def db_query_log(name,action,new_state):
    cnx = db_getdbconnection()
    cursor = cnx.cursor()

    query = "INSERT INTO `ist176550`.`LOGS` (`name`, `action`, `new_state`) VALUES (%s,%s,%s);"
    items = (name,action,new_state)
    cursor.execute(query, items)
    cnx.commit()

    cursor.close()
    cnx.close()


def db_query_add_user(name, istID, uid_hash, group):
    cnx = db_getdbconnection()
    cursor = cnx.cursor()

    values = '(' + str(name) + ',' + str(istID) + ',' + uid_hash + ',' + group + ')'
    print(values)

    query = "INSERT INTO `ist176550`.`AUTHORIZED_STUDENTS` (`Name`, `istID`, `hashUID`, `Group`) VALUES (%s , %s , %s , %s);"

    cursor.execute(query, (name, istID, uid_hash, group))
    cnx.commit()

    cursor.close()
    cnx.close()


def main():
    if (db_getdbconnection() != False):
        print ("connected to db")
        query = "SELECT * FROM ist176550.DAILY_REGISTER;"
        result = db_query(query)

        for (id, istID, timeStamp) in result:
            print ("ID " + str(istID) + " " + "timeStamp" + str(timeStamp))

# main()
# db_query_add_user("jjo","ist64455","jh44kjh","a")
