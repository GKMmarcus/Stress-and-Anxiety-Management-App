from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
import requests

app = Flask(__name__)

app.secret_key = 'cheese'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mental_health_db'

mysql = MySQL(app)


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST" and 'email' in request.form and 'password' in request.form:
        email = request.form["email"]
        password = request.form["password"]

        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email,password,))
        users = cursor.fetchone()

        if users:
            session['loggedin'] = True
            session['user_id'] = users['user_id']
            session['email'] = users['email']
            return redirect(url_for("home"))
        else:
            return 'Incorrect Email/Password'

    return render_template("index.html", error=error)

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method =='POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s',(email,))
        users = cursor.fetchone()

        if users:
            return "Account already exists"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return "Invalid Email"
        elif not name or not password or not email:
            return "Please fill out the form"
        else:
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()

            cursor.execute('INSERT INTO users (name,password,email) VALUES (%s,%s,%s)',(name,password,email,))
            mysql.connection.commit()

            return "Register Success"
        
    elif request.method == 'POST':
        return "Please Fill out the form"
    
    return render_template('register.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/profile")
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users where user_id = %s',(session['user_id'],))
        users = cursor.fetchone()

        return render_template("profile.html", users = users)
    
    return redirect(url_for('login'))

@app.route("/meditate")
def meditate():

    meditate_api_key = 'AIzaSyBc9ip6gDo7wNzlPPiLC4-JzXWSfd9W-wQ'
    SEARCH_QUERY = "guided meditation"
    MAX_RESULTS = 5

    reponse = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={SEARCH_QUERY}&maxResults={MAX_RESULTS}&type=video&key={meditate_api_key}")
    data = reponse.json()

    for item in data["items"]:
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Title: {title}\nURL: {video_url}\n")

    return render_template('meditate.html')

@app.route
def profile():
    return render_template('profile.html')

if __name__ == "__main__":
    app.run(debug=True)