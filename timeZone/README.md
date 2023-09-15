# Time Tracker website
#### Video Demo:  <https://youtu.be/KSAIedkNQIk?si=1RwWqpozcYsjzc8i>
#### Description:
The site lets you store different timeZones from all over the world. If it is not available on my data base then you can search directly from the api(did not impliment a save option for the api). user can store time zones (displayed on index page). The reason why i made a data base for location names was to make things simple for the end user as the time API formating could get complication and i felt that this is more user friendly. I also tried to make the website let the user no what was going on and tried to have leading messages. e.g no location found try a custom location... i also made a time data class to make sure that the data being sent had all the necissary fields. This was also an oportunity for me to play around with classes which i havent done in python. The reason why i didnt store custome lcoations directly from the api is because i had a foerign key error in my stored locations table. For the most part the sql it tidely laid out with the user table having a hashed password for security reasons.

templates - holds all of the html templates

app.py - handles all the data transfer to the template folders and also querys the data base and calls functions from the helpers.py

helpers.py - handles all the heavy work like sql connection and api connection. there are two main functions for this
lookup(latitude, longitude)- returns the data from api to do with a given latitude and longitude.

getData(locationName) - takes a location name and sends it to the api. if match returns all needed paramerters


data base schema
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,username TEXT NOT NULL,hashPassword TEXT NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE locations (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, latitude TEXT NOT NULL, longitude TEXT NOT NULL, locationName TEXT NOT NULL);
CREATE TABLE storedLocations (userID int NOT NULL,locationID int NOT NULL,FOREIGN KEY (userID) REFERENCES users(id)FOREIGN KEY (locationID) REFERENCES locations(id));
CREATE TABLE customLocations(id INTEGER PRIMARY KEY, latitude INTEGER NOT NULL, longitude INTEGER NOT NULL, userID INTEGER, name TEXT, FOREIGN KEY (userID) REFERENCES users(id));


