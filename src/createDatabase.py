# Import SQLite3 database library
import sqlite3

# Import the os library to have the database in seperate dir
import os

# Join the current dir with database dir, store in variable for connection
databasePath = os.path.join(os.path.dirname(__file__), "../resources/userDB.db")

def createDatabase():
    # Connect to db
    conn = sqlite3.connect("databasePath")
    print ("Opened database successfully")

    # Create table within db
    conn.execute("CREATE TABLE USERS (ID INT PRIMARY KEY);")

    # Save changes
    conn.commit()
    print ("Table created successfully")

    # TESTING
    conn.execute("SELECT ID FROM USERS")

    # Close db connection
    conn.close()
