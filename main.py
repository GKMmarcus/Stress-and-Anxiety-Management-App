from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy user data for login
USER_CREDENTIALS = {
    "test@example.com": "password123"
}

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        if email in USER_CREDENTIALS and USER_CREDENTIALS[email] == password:
            return redirect(url_for("home"))  # Redirect on successful login
        else:
            error = "Invalid email or password"

    return render_template("index.html", error=error)

@app.route("/home")
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)