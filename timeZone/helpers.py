
import requests
from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
def getData(locationName):
    print("locattionName",locationName)
    url = (
        #"https://timeapi.io/api/Time/current/zone?timeZone=Europe/Amsterdam"
        f"https://timeapi.io/api/Time/current/zone?timeZone={locationName}"
    )
    try:
        req = requests.get(url)
        if req.status_code == 400:
            message = "Invalid Location"
            return message
        if req.status_code != 200:
            print("Request faild with status code:", req.status_code)
            return None
        data = req.json()
        time = data["time"],
        day = data["dayOfWeek"],
        date = data["date"]
        timeZone = data["timeZone"]
        Info = []
        Info.append(time)
        Info.append(day)
        Info.append(date)
        Info.append(timeZone)
        print("this is info",Info)
        return Info
    except(requests.RequestException, ValueError, KeyError, IndexError):
        return None

def lookup(latitude, longitude):
    # TimeZone API
    url = (
        f"https://timeapi.io/api/Time/current/coordinate?latitude={latitude}&longitude={longitude}"
    )
    # Query API
    try:
        req = requests.get(url)
        if req.status_code != 200:
            print("Request faild with status code:", req.status_code)

        data = req.json()
        time = data["time"],
        day = data["dayOfWeek"],
        date = data["date"]
        timeZone = data["timeZone"]
        Info = []
        Info.append(time)
        Info.append(day)
        Info.append(date)
        Info.append(timeZone)
        return Info
    except(requests.RequestException, ValueError, KeyError, IndexError):
        return None






class time_data():
    def __init__(self, time,day,date,timeZone, name):
        self.time = time
        self.day = day
        self.date = date
        self.name = name
        self.timeZone = timeZone




