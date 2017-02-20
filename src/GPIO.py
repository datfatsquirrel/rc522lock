import os, sys
# Add the directory "lib/rfid" to the sys.path array to make it available for Python
sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/MFRC522-python"))
# Create a variable with the path for the userDB database
dbDir = os.path.join(os.path.dirname(__file__), "../resources/main.db")

# Allows me to create delays and get the current time when gathering data for database
from time import sleep, gmtime, strftime

# Database library
import sqlite3

# Library to control GPIO board
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

# Library for the RC522 RFID reader
# https://github.com/mxgxw/MFRC522-python/
import MFRC522

def scan():
    # Create an object of MFRC522 - allows me to scan for cards, read the UID of the card and authenticate it
    reader = MFRC522.MFRC522()

    # Loop to keep scanning for tags/cards
    while True:
        # Sends a request to the reader to see if a card is present
        (status,TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

        # If no card is found then it will continue the loop
	    # If a card is present the program will run the following 'if' statement
        if status == reader.MI_OK:

            # Read the UID of the card, ready to query the database.
            (status,uid) = reader.MFRC522_Anticoll()

    	    # Take the values in 'uid' list and concatenate into a string for database query
    	    uidStr = ""
    	    for number in uid:
    	        uidStr = uidStr + str(number)
    	    print int(uidStr)

            if uidStr == "7660887599":
                # Tag was master card
                success = "Master card"
                time.sleep(2)
                masterCard()
            else:
                isValid = queryUID(uidStr)

        	if isValid == True:
                # Tag was valid
                success = "True"

                # Log the time at which the tag was used
                logTime(status, id, success)

        	    # Change the state of the door to it's opposite state
        	    operateDoor(uidStr)

        	    state = GPIO.input(3)
        	    if state == 0:
    	    	    # Delay to scan after 2 seconds to see if the RFID signal is still present
                        time.sleep(2)

        	    	# Take the current time (seconds since Jan 1st 1970) and store as a temp value
        	    	tempTimeVal = time.time()

        	    	# Set the default mode to lock automatically after the door is unlocked
        	    	changeState = True

        	    	# Create a loop which runs for 0.5 seconds to scan for RFID signals
        	    	while (time.time() - tempTimeVal) < 0.5:
        	    	    (status,TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

        		    # Check if card is still present
        		    if status == reader.MI_OK:

        		    	# Set the door to stay unlocked once originally unlocked
        		    	changeState = False

        	    	# Automatically lock the door if changeState is it's default value (True)
        	    	if changeState == True:
        		    operateDoor(uidStr)
            else
                # Tag was invalid
                success = "False"

                # Get the current status of the door so after the LED has flashed it can return to its original status
                GPIO.setmode(GPIO.BCM)
                locked = GPIO.input(GPIO.13)
                flash = 3

                # Flash the red LED to indicate a failed attempt
                while flash != 0
                    GPIO.output(13, GPIO.HIGH)
                    time.sleep(0.1)
                    GPIO.output(13, GPIO.LOW)
                    time.sleep(0.1)
                if locked == 1
                    GPIO.output(13, GPIO.HIGH)

        # Delay for 3 seconds before the script can be run again
	    time.sleep(2)

def queryUID(id):
    # Connect to the user database
    conn = sqlite3.connect(dbDir)
    curs = conn.cursor()

    # Check if the UID exists in the database
    returnValue = curs.execute("SELECT ID FROM USERS WHERE ID = "+id).fetchone()
    conn.close()

    # Returns true if valid, false if invalid
    if returnValue is not None:
        return True
    else:
        return False

def masterCard():
    print "Master card activated."

    # Turn both green and red LEDs on to indicate that the Master card has been used
    GPIO.setmode(GPIO.BCM)
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(26, GPIO.HIGH)

    # See comments between line 24 and 44
    reader = MFRC522.MFRC522()
    continueLoop = True
    while continueLoop == True:
        (status,TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
        if status == reader.MI_OK:
            (status,uid) = reader.MFRC522_Anticoll()
            uidStr = ""
    	    for number in uid:
    	        uidStr = uidStr + str(number)
    	    print int(uidStr)

            # If the master card is used again, exit the administrative mode
            if uidStr == "7660887599":
                state = GPIO.input(3)

                # Change LEDs back to original state
                if state == 0:
                    GPIO.output(26, GPIO.LOW)
                    GPIO.output(13, GPIO.HIGH)
                elif state == 1:
                    GPIO.output(26, GPIO.HIGH)
                    GPIO.output(13, GPIO.LOW)
                continueLoop = False
            else:
                # Connect to the user database
                conn = sqlite3.connect(dbDir)
                curs = conn.cursor()

                # Check if the UID is in the database
                returnValue = curs.execute("SELECT ID FROM USERS WHERE ID = "+uidStr).fetchone()
                print returnValue
                conn.close()

                # If the UID is in the database, remove it
                if returnValue is not None:
                    print "Remove."
                    rmUID(uidStr)
                    continueLoop = False

                # If the UID is not in the database, add it
                else:
                    print "Add."
                    addUID(uidStr)
                    continueLoop = False
    print "Master card deactivated."

def addUID(id):
    # Connect to the database
    conn = sqlite3.connect(dbDir)
    curs = conn.cursor()

    # Insert the UID into the database
    curs.execute("INSERT INTO USERS (ID) VALUES ("+id+")")
    conn.commit()
    conn.close()

def rmUID(id):
    # Connect to the database
    conn = sqlite3.connect(dbDir)
    curs = conn.cursor()

    # Remove the UID from the database
    curs.execute("DELETE FROM USERS WHERE id = "+id)
    conn.commit()
    conn.close()

def operateDoor(id):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(3, GPIO.OUT)
    state = GPIO.input(3)

    # Lock door, turn green LED off and red LED on
    if state == 0:
        GPIO.output(26, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(3, GPIO.HIGH)
        logTime(status, id, success)

    # Unlock door, turn green LED on and red LED off
    elif state == 1:
        GPIO.output(26, GPIO.HIGH)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(3, GPIO.LOW)
        logTime(status, id, success)

def logTime(status, id):
    # Get the current time and date as a string
    currentTime = strftime("%a, %d %b %Y, %H:%M:%S", gmtime())

    # Connect to the database
    conn = sqlite3.connect(dbDir)
    curs = conn.cursor()
    print status + id + currentTime

    # Insert UID, time and status of the door into database
    curs.execute("INSERT INTO LOGS (UID, TIME, STATUS, SUCCESS) VALUES ("+id+", "+currentTime+", "+status+", "+success+")")

scan()
