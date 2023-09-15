from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL
from flask_session import Session
from helpers import apology, login_required, lookup,time_data, format, getData
from werkzeug.security import check_password_hash, generate_password_hash
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///timezone.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

@app.route("/queryAPI", methods=["GET", "POST"])
def queryAPI():
    if request.method == "POST":
        if not request.form.get("location"):
            return apology("must provide name", 400)
        location = request.form.get("location")
        #call api
        Info = getData(location)
        print("this is info",Info)
        if Info == "Invalid Location":
            noData = True
            return render_template("QueryAPI.html",status=noData)
        #print("this is data sent",Info)
        data = []
        data.append(time_data(Info[0],Info[1],Info[2],Info[3],location))
        print("This has been run")
        return render_template("QueryAPI.html", found = True,data=data)
        #return render_template("QueryAPI.html")
    else:
        return render_template("QueryAPI.html")


#index
@app.route("/")
@login_required
def index():
    # make a table to display users
    #get stored locations
    rows_stored = db.execute("SELECT locations.latitude, locations.longitude, locations.locationName FROM storedLocations JOIN users ON storedLocations.userID=users.id JOIN locations ON storedLocations.locationID = locations.id WHERE storedLocations.userID=2")
    #rows = db.execute("SELECT locations.latitude, locations.longitude, locations.locationName FROM storedLocations JOIN users ON storedLocations.userID=users.id JOIN locations ON storedLocations.locationID = locations.id WHERE storedLocations.userID =?",session["user_id"])
    # get custom locations
    rows_custom = db.execute("SELECT customLocations.latitude, customLocations.longitude, customLocations.name FROM storedLocations JOIN users ON storedLocations.userID=users.id JOIN customlocations ON storedLocations.locationID = customlocations.id WHERE storedLocations.userID=2")
    data = []
    Info = []
    for row in rows_stored:
        lat = row["latitude"]
        long = row["longitude"]
        name = row["locationName"]
        Info = lookup(lat,long)
        data.append(time_data(Info[0],Info[1],Info[2],Info[3],name))
        Info = []
    for row in rows_custom:
        lat = row["latitude"]
        long = row["longitude"]
        name = row["name"]
        Info = lookup(lat,long)
        data.append(time_data(Info[0],Info[1],Info[2],Info[3],name))
    return render_template("index.html", data=data)
#SELECT locations.latitude, locations.longitude, locations.locationName FROM storedLocations JOIN users ON storedLocations.userID=users.id JOIN locations ON storedLocations.locationID = locations.id WHERE storedLocations.userID =?",session["user_id"];

#login
@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hashPassword"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



#register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method =="POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        if not request.form.get("password"):
            return apology("must provide password", 400)
        password = request.form.get("password")
        passwordConfirm = request.form.get("confirmation")
        if password != passwordConfirm:
            return apology("password is different", 400)
        hash = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users ('username', 'hashPassword' )VALUES (?, ?)",request.form.get("username"),hash)
        except:
            return apology("username already exists")
        return redirect("/")

    else:

        return render_template("register.html")

#add location
@app.route("/add", methods=["GET", "POST"])
def addLocation():

    if request.method == "POST":
        rows = db.execute("SELECT id, locationName FROM locations WHERE locationName =?",request.form.get("location").lower())
        if not rows:
            noData = True
            return render_template("add.html",status=noData)

        else:
            location_id = rows[0]["id"]
            db.execute("INSERT INTO storedLocations (userID,locationID) VALUES (?,?)",session["user_id"],location_id)
            flash("Successfully Added")
            return render_template("add.html")
    else:
        noData = False
        return render_template("add.html")
#add custom location
@app.route("/addcustom", methods=["GET", "POST"])
def addCustome():
    if not request.form.get("latitude"):
        return apology("input field no filled in")
    if not request.form.get("longitude"):
        return apology("input field no filled in")
    if not request.form.get("name"):
        return apology("must input name for custome location")
    lat = int(request.form.get("latitude"))
    long = int(request.form.get("longitude"))
    name = request.form.get("name")
    if lat < -90 or lat > 90:
        return apology("must be number between -90 and 90")
    if long < -180 or long > 180:
        return apology("must be number between -90 and 90")

    db.execute("INSERT INTO customLocations (userID,latitude,longitude, name) VALUES (?,?,?,?)",session["user_id"],lat,long,name)
    #insert into stored locations
    rows = db.execute("SELECT id FROM customLocations WHERE name =? and userID = ?",name,session["user_id"])
    location_id = rows[0]["id"]
    db.execute("INSERT INTO storedLocations (userID,locationID) VALUES (?,?)",session["user_id"],location_id)
    flash("Successfully created custom location")
    return render_template("add.html")




