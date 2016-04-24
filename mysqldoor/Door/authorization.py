import mysqljoao


def door_get_authorized():
    query = "SELECT istID FROM AUTHORIZED_STUDENTS;"
    return mysqljoao.db_query(query)


def door_get_logged_in():
    query = "SELECT istID FROM DAILY_REGISTER;"
    return mysqljoao.db_query(query)


def door_get_ellegible():
    query = "SELECT    name,AUTHORIZED_STUDENTS.istID, AUTHORIZED_STUDENTS.hashUID  FROM ist176550.AUTHORIZED_STUDENTS " \
            "JOIN DAILY_REGISTER where (AUTHORIZED_STUDENTS.istID = DAILY_REGISTER.istID);"

    result = mysqljoao.db_query(query)

    return result

def door_log(name,action,new_state):
    mysqljoao.db_query_log(name,action,new_state)
    return

def test():
    result = door_get_ellegible()
    if not result.fetchone():
        print("VAZIOOO")
    for (name, ist_ID, hash) in result:
        print("Electible " + str(ist_ID) + " hash " + str(hash))

#uncomment for testing
#test()
#door_log("joao","lockkk","kajhd")