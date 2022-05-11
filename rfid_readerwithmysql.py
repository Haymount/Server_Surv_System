import RPi.GPIO as GPIO
import mfrc522 as MFRC522
import signal
import time
import MySQLdb
from time import gmtime, strftime
from datetime import date


continue_reading = True

firstname = ""
lastname = ""

db = MySQLdb.connect("localhost", "root", "fedtfirma42", "rfiddb")

_currTime = strftime("%H:%M:%S", gmtime())
_currDate = date.today().strftime("%Y-%m-%d")

GPIO.setmode(GPIO.BCM)
LEDred = 14
GPIO.setup(LEDred, GPIO.OUT, initial=GPIO.HIGH)
LEDgreen = 18
GPIO.setup(LEDgreen, GPIO.OUT, initial=GPIO.LOW)

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Kast med kortet/Chippen bror")
print("Press Ctrl-C to stop.")


# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        # print "Card detected"
        pass

    # Get the UID of the card
    (status, uid) = MIFAREReader.MFRC522_Anticoll()
    cur = db.cursor()

    _uid = +str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+','+str(uid[4])
    # This is the default key for authentication
    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        # Print UID
        print(_uid)



    # Check if UID is in DB
    cur.execute("SELECT * FROM users WHERE uid = %s", (_uid,))

        # Read data
    for row in cur.fetchall():
        firstname = str(row[1])
        lastname = str(row[2])

        # Read time and date
    _currTime = strftime("%H:%M:%S", gmtime())
    _currDate = date.today().strftime("%Y-%m-%d")

        # Send out a greeting to print name and date
    print("Hello " + firstname + " " + lastname)
    print(_currDate + " " + _currTime)

      # Insert every login into database
    try:
        cur.execute("INSERT INTO log (uid,fname,lname,_date,_time) VALUES (%s,%s,%s,%s,%s)",
                    (_uid, firstname, lastname, _currDate, _currTime))
        db.commit()
    except (db.Error, db.Warning) as e:
        print(e)
    finally:
        print("Successful")
        cur.close()

      # Select the scanned tag
    MIFAREReader.MFRC522_SelectTag(uid)

      # Authenticate
    status = MIFAREReader.MFRC522_Auth(
        MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

      # Check if authenticated
    if status == MIFAREReader.MI_OK:
        MIFAREReader.MFRC522_Read(8)
        MIFAREReader.MFRC522_StopCrypto1()
    else:
        pass

db.close()