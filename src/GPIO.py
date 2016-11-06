# Add the directory "lib/rfid" to the sys.path array to make it available for Python
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/rfid"))

# Library to allow me to control the GPIO pins on the RPi
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO")
   
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
    loop =  True
    while loop:
 
        '''
       - Send a request to the reader to scan for any present RFID cards/tags.
       - 'status' is used to verify the status of the reader (if the user has tapped a card/tag) .
       - 'TagType' is used to validate that the present card/tag is a MIFARE card.
       - This variable doesn't have to be used as it would only be used to warn the user, however because there is no console for the user there is not much need for this.
       '''
       
        (status,TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
 
        # This checks if a card was found. If no card is found then it will continue the loop.
        if status == reader.MI_OK:
 
            # Read the UID of the card, ready to query the database.
            (status,uid) = reader.MFRC522_Anticoll()
	    print uid

	    # Take the values in 'uid' list and concatenate into a string for database query
	    uidStr = ""
	    for number in uid:
	        uidStr = uidStr + str(number)
	    print int(uidStr)


''' 
            # Query the database for the UID to see if it is valid.
            queryUID()
 
def queryUID():
   
    # Connect to the user database
    conn = sqlite3.connect('userDB.db')
'''

scan()
