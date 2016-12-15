# 1. Add the directory "lib/rfid" to the sys.path array to make it available for Python
# 2. Create a variable with the path for the userDB database
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/MFRC522-python"))
dbDir = os.path.join(os.path.dirname(__file__), "../resources/userDB.db")

import time, sqlite3

# Library to allow me to control the GPIO pins on the RPi
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO")

GPIO.setwarnings(False)

# Library for the RC522 RFID reader
# https://github.com/mxgxw/MFRC522-python/
try:
    import MFRC522
except RuntimeError:
    print("Error importing MFRC522")

def scan():

    # Create an object of MFRC522 which will allow me to scan for cards, read the UID of the card and authenticate it.
    reader = MFRC522.MFRC522()

    # Loop to keep scanning for tags/cards
    while True:

        '''
       - Send a request to the reader to scan for any present RFID cards/tags.
       - 'status' is used to verify the status of the reader (if the user has tapped a card/tag) .
       - 'TagType' is used to validate that the present card/tag is a MIFARE card.
       - This variable doesn't have to be used as it would only be used to warn the user, however because there is no console for the user there is not much need for this.
       '''
        # Check if a card is present
        (status,TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

        # If no card is found then it will continue the loop
	    # If a card is present the program will run this if statement
        if status == reader.MI_OK:

            # Read the UID of the card, ready to query the database.
            (status,uid) = reader.MFRC522_Anticoll()
    	    print uid

    	    # Take the values in 'uid' list and concatenate into a string for database query
    	    uidStr = ""
    	    for number in uid:
    	        uidStr = uidStr + str(number)
    	    print int(uidStr)

            if uidStr == "7660887599":
                time.sleep(2)
                masterCard()
            else:
                isValid = queryUID(uidStr)

        	if isValid == True:
        	    # Change the state of the door to it's opposite state
        	    operateDoor()

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
        		    operateDoor()

        # Delay for 3 seconds before the script can be run again
	    time.sleep(2)

def queryUID(id):

    # Connect to the user database
    conn = sqlite3.connect(dbDir)
    curs = conn.cursor()
    returnValue = curs.execute("SELECT id from USERS where id = "+id).fetchone()
    conn.close()
    if returnValue is not None:
        return True
    else:
        return False

def masterCard():
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
            if uidStr == "7660887599":
                continueLoop = False
            else:
                # Connect to the user database
                conn = sqlite3.connect(dbDir)
                curs = conn.cursor()
                returnValue = curs.execute("SELECT id from USERS where id = "+uidStr).fetchone()
                print returnValue
                conn.close()
                if returnValue is not None:
                    print "Remove."
                    rmUID(uidStr)
                    continueLoop = False
                else:
                    print "Add."
                    addUID(uidStr)
                    continueLoop = False

def addUID(id):
    conn = sqlite3.connect(dbDir)
    curs = conn.cursor()
    curs.execute("INSERT INTO USERS VALUES ("+id)
    conn.close()

def rmUID(id):
    conn = sqlite3.connect(dbDir)
    curs = conn.cursor()
    curs.execute("DELETE FROM USERS WHERE id = "+id)
    conn.close()

def operateDoor():
    GPIO.setup(3, GPIO.OUT)
    state = GPIO.input(3)
    if state == 0:
	    GPIO.output(3, GPIO.HIGH)
    elif state == 1:
        GPIO.output(3, GPIO.LOW)

scan()
