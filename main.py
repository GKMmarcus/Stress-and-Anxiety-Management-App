from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector

app = Flask(__name__)
app.secret_key ='Monkey'

mydb = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    database = 'mental_health_db'
)

cursor = mydb.cursor()

@app.route('/login', methods=['GET','Post'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        cursor.execute('SELECT * FROM users Where email = %s AND password = %s')
        users = cursor.fetchchone()

        if users:
            session['id'] = users[0]
            session['email'] =  users[1]
    return render_template("index.html")