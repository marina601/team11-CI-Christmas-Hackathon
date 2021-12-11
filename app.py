import os
from flask import (
    Flask, flash, render_template, redirect,
    request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sslify import SSLify
if os.path.exists("env.py"):
    import env

app = Flask(__name__)
sslify = SSLify(app)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    """
    Find Products from Mongo db collection
    """
    wishes = mongo.db.wishes.find()

    return render_template("home.html", wishes=wishes)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Checking if the user already exists,
    If not, then checking if username exists
    Checking if password_1 = password_2
    Creating a dictionary to insert user into db
    Insert the new user into db
    Put the user into 'session' cookie
    Redirect the user to their profile page
    """
    groups = list(mongo.db.groups.find().sort("group_name", 1))

    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username in use, try alternative")
            return redirect(url_for("register"))
        
        # Validate email
        existing_email = mongo.db.users.find_one(
            {"email": request.form.get("email")}
        )

        if existing_email:
            flash("This email address already exists")
            return redirect(url_for("login"))

        password_1 = request.form.get("password")
        password_2 = request.form.get("password_2")

        if password_1 != password_2:
            flash("Your passwords do not match")
            return redirect(url_for("register"))
        
        email = request.form.get("email")

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "email": request.form.get("email"),
            "group_name": request.form.get("group_name")
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("You have successfully Registered!")
        return redirect(url_for('index', username=session["user"]))
    
    # Page Title
    title = 'Register'
    return render_template("register.html", title=title, groups=groups)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login route
    Check if user exists in the database
    Check if password matches user input
    Redirects user to home page
    Otherwise error message displayed
    """
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(existing_user
                                   ["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}"
                      .format(request.form.get("username").capitalize()))
                return redirect(url_for(
                    'index', username=session["user"]))

            else:
                # invalid password match
                flash("You have enetered incorrect Username and/or Password")
                return redirect(url_for('login'))

        else:
            # invalid username match
            flash("You have entered incorrect Username and/or Password")
            return redirect(url_for('login'))

    # if the user is already in session
    if 'user' in session:
        return redirect(url_for('index', username=session['user']))

    # Page Title
    title = 'Login'
    return render_template("login.html", title=title)

@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
