import hashlib
import ReadSala2
import mysqljoao

name = "nono"
istID = "nono"
uid_hash = "nono"
group = "nono"

def get_ist_id():
    global istID
    global name
    global group

    istID = raw_input("Indique o istID: ist1xxxxx \n")
    while "ist" not in istID:
        istID = raw_input("O input nao obecede ao formato ist1xxxxx, tente de novo \n")

    name = raw_input("Indique o nome do novo utilizador \n")

    group= raw_input("Indique o grupo (a,b,c) \n")

    print("Resumo:")
    print("-Nome:   "+name)
    print("-istID:  "+istID)
    print("-Grupo:  "+group)

    print("\n prima enter para continuar...")
    raw_input()



def add_user_to_db():
   mysqljoao.db_query_add_user(name,istID,uid_hash,group)


get_ist_id()
uid = ReadSala2.get_uid()
print ("UID do cartao: "+str(uid))
uid_hash = ReadSala2.get_digest(uid)
print ("Hash do cartao: "+str(uid_hash))
print ("Prima enter para continuar")
raw_input()
add_user_to_db()

