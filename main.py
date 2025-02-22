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
        password = request.form['password'].encode('utf-8')

        cursor.execute('SELECT * FROM users Where email = %s',(email,))
        user = cursor.fetchchone()

        if user:
            stored_password = user[3].encode('utf-8')

            session['id'] = user[0]
            session['email'] =  user[2]
            return "Login Good"
        
        return "Invalid Email/Password"
        
    return render_template("index.html")