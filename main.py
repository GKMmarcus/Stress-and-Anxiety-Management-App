from flask import Flask, render_template, request, redirect, url_for,session,jsonify
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
            error = 'Incorrect Email/Password'

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

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('name', None)

    return redirect(url_for('login'))

@app.route("/home")
def home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users where user_id = %s',(session['user_id'],))
    users = cursor.fetchone()

    return render_template('home.html', users = users)
    
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
    video_urls = []

    if "items" in data:
        for item in data["items"]:
            if "id" in item and "videoId" in item["id"]:
                video_id = item["id"]["videoId"]
                video_urls.append(f"https://www.youtube.com/embed/{video_id}")

    if video_urls:
        return render_template('meditate.html', video_urls=video_urls)
    else:
        return "No embeddable videos found.", 404
    
@app.route("/breathing")
def breathing():

    meditate_api_key = 'AIzaSyBc9ip6gDo7wNzlPPiLC4-JzXWSfd9W-wQ'
    SEARCH_QUERY = "breathing exercise"
    MAX_RESULTS = 5

    reponse = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={SEARCH_QUERY}&maxResults={MAX_RESULTS}&type=video&key={meditate_api_key}")
    
    data = reponse.json()
    video_urls = []

    if "items" in data:
        for item in data["items"]:
            if "id" in item and "videoId" in item["id"]:
                video_id = item["id"]["videoId"]
                video_urls.append(f"https://www.youtube.com/embed/{video_id}")

    if video_urls:
        return render_template('breathing.html', video_urls=video_urls)
    else:
        return "No embeddable videos found.", 404
    
@app.route('/journal', methods = ['GET','POST'])
def journal():
    if request.method == 'POST':
        user_id = session['user_id']
        mood = request.form['mood']
        notes = request.form['notes']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO journal(user_id, mood, notes) VALUES (%s,%s,%s)',(user_id, mood, notes,))
        mysql.connection.commit()
        

        return redirect(url_for('journal'))
        
    return render_template('journal.html')

@app.route('/test', methods = ['GET','POST'])
def test():
    if request.method == 'POST':
        data = request.json
        answers = data.get('answers', [])

        total_score = sum(answers)

        if total_score <= 10:
            stress_level = "Low Stress"
        elif total_score <= 20:
            stress_level = "Moderate Stress"
        elif total_score <= 30:
            stress_level = "High Stress"
        else:
            stress_level = "Severe Stress"
            
        return jsonify({"message": "Test submitted successfully", "stress_level": stress_level, "score": total_score})
    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)