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

cursor = mydb.cursor(dictionary=True)

@app.route('/login', methods=['GET','Post'])
def login():
    if request.method == "POST" :
        email = request.form['email']
        password = request.form['password']

        cursor.execute('SELECT * FROM users WHERE email = %s AND password =%s',(email,password,))
        user = cursor.fetchone()

        if user:
            session['loggedin'] = True
            session['id'] = user['user_ID']
            session['email'] =  user['Email']
            return "Login Good"
        
        return "Invalid Email/Password"
        
    return render_template("index.html")