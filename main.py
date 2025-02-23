from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.secret_key ='Monkey'
bcrypt = Bcrypt(app)


mydb = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    database = 'mental_health_db'
)

cursor = mydb.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":

        email = request.form['email']
        password = request.form['password']

        cursor.execute('SELECT * FROM users WHERE email = %s',(email,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user[3], password):
            session['id'] = user[0]
            session['email'] =  user[2]
            return "Login Good"
        else:
            return "Invalid Email/Password"
        
        
    return render_template("index.html")