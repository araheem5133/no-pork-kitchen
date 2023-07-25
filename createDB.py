import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Youshallnotpass!", # Change accordingly
)

mycursor = mydb.cursor()

mycursor.execute("DROP database IF EXISTS NoPorkKitchenDB")
mycursor.execute("CREATE database NoPorkKitchenDB")

#mycursor.execute("SHOW databases")
#for db in mycursor:
#    print(db);

mycursor.close()
mydb.close()