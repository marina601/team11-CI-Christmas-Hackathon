import os
import pymongo
from flask import (
    Flask, flash, render_template, redirect,
    request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sslify import SSLify
from datetime import date
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


@app.route("/add_group", methods=["GET", "POST"])
def add_group():
    """Create a new group"""
    if request.method == "POST":
        # Check for existing group names
        existing_group = mongo.db.groups.find_one(
            {"group_name": request.form.get("group_name")}
        )

        if existing_group:
            flash("This group name already exists, choose another one")
            return redirect(url_for("add_group"))

        group = {
            "group_name": request.form.get("group_name")
        }
        mongo.db.groups.insert_one(group)
        flash("New Group Created!")
        return redirect(url_for("register"))

    return render_template("add_group.html")

@app.route("/add_wish", methods=["GET", "POST"])
def add_wish():
    """
    Add a new wish
    get all the input fields from the form
    create a new wish in the database
    """
    # find the current date
    today = date.today()
    # find the current user group name
    user_group = mongo.db.users.find_one(
        {"username": session["user"]})["group_name"]
    # find the users under the same group name
    users = mongo.db.users.find({'group_name':user_group})
    if request.method == "POST":
        wish = {
            "message": request.form.get("message"),
            "for_date": request.form.get("for_date"),
            "username_from": session["user"],
            "created_date": str(today),
            "group_name": user_group,
            "for_username": request.form.get("for_username"),
        }
        mongo.db.wishes.insert_one(wish)
        flash("Wish Successfully Created")
        return redirect(url_for("index"))
   
    return render_template("add_wish.html", user_group=user_group, users=users)


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the seeion user's username from db
    # Page Title
    title = 'Profile'

    wishes = list(mongo.db.wishes.find())

    if 'user' in session:
        username = mongo.db.users.find_one(
            {"username": username})["username"].capitalize()

        wishes = list(mongo.db.wishes.find(
                           {"username_from": session["user"]}))
    else:
        flash('You must be logged in!')
        return redirect(url_for('login'))

    return render_template(
                "profile.html", username=username,
                wishes=wishes, title=title)


@app.route("/delete_wish/<wish_id>")
def delete_wish(wish_id):
    """
    Delete a wish from the database
    Redirect the user back to profile page
    """
    wish = mongo.db.wishes.find_one({"_id": ObjectId(wish_id)})
    mongo.db.wishes.delete_one({"_id": ObjectId(wish_id)})
    flash("Your wish has been Deleted")

    return redirect(url_for('profile', username=session['user']))

@app.route("/edit_wish/<wish_id>", methods=["GET", "POST"])
def edit_wish(wish_id):
    """
    Edit wish route
    Update the user wish based on wish_id
    """
    # find the current user group name
    user_group = mongo.db.users.find_one(
        {"username": session["user"]})["group_name"]
    
    if request.method == "POST":
        submit = {
            "message": request.form.get("message"),
            "for_date": request.form.get("for_date"),
            "username_from": session["user"],
            "group_name": user_group,
            "for_username": request.form.get("for_username"),
        }
        mongo.db.wishes.update({"_id": ObjectId(wish_id)}, submit)
        flash("Your Wish Has Been Successfully Updated")
        return redirect(url_for('profile', username=session["user"]))

    wish = mongo.db.wishes.find_one({"_id": ObjectId(wish_id)})
    users = mongo.db.users.find({'group_name':user_group})

    # Page Title
    title = 'Edit-Wish'
    return render_template("edit_wish.html", wish=wish,
                           users=users, user_group=user_group, title=title)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
