import mysql.connector

mydb = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
)

if mydb.is_connected():
    print("Connection Good")
else:
    print("Connection Bad")