import RPi.GPIO as GPIO
import mfrc522 as MFRC522
import signal
import time
import MySQLdb
import mysql.connector
from time import gmtime, strftime
from datetime import date
from mfrc522 import SimpleMFRC522


continue_reading = True

#firstname = ""
#lastname = ""

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="fedtfirma42",
  database="rfiddb"
  )

cursor = db.cursor()

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

#reader = ()
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

reader = SimpleMFRC522()

# Welcome message
print("Kast med kortet/Chippen bror")
print("Press Ctrl-C to stop.")

try:
  while True:
    id, text = reader.read()

    cursor.execute("Select id, name FROM users WHERE rfid_uid="+str(id))
    result = cursor.fetchone()
    
    

    if cursor.rowcount >= 1:
      print("Welcome " + result[1])
      cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],) )
      db.commit()
    else:
      print("User does not exist.")
    time.sleep(2)
finally:
  GPIO.cleanup()



# This loop keeps checking for chips. If one is near it will get the UID and authenticate
#while continue_reading:
    # This is the default key for authentication
#    key = [0xFF, 0xFF, 0xFF,0xFF,0xFF]
    # Scan for cards
 #   (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
  #  if status == MIFAREReader.MI_OK:
        # print "Card detected"
   #     pass

    # Get the UID of the card
    #(status, uid) = MIFAREReader.MFRC522_Anticoll()
    #cur = db.cursor()

    
    # If we have the UID, continue
    #if status == MIFAREReader.MI_OK:
        # Print UID
     #   print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+','+str(uid[4]))



    # Check if UID is in DB
    #cur.execute("SELECT * FROM users WHERE uid = %s", (uid))

        # Read data
    #for row in cur.fetchall():
     #   firstname = str(row[1])
      #  lastname = str(row[2])

        # Read time and date
    #_currTime = strftime("%H:%M:%S", gmtime())
    #_currDate = date.today().strftime("%Y-%m-%d")

        # Send out a greeting to print name and date
    #print("Hello " + firstname + " " + lastname)
    #print(_currDate + " " + _currTime)

      # Insert every login into database
    #try:
     #   cur.execute("INSERT INTO log (uid,fname,lname,_date,_time) VALUES (%s,%s,%s,%s,%s)",
      #              (_uid, firstname, lastname, _currDate, _currTime))
       # db.commit()
    #except (db.Error, db.Warning) as e:
     #   print(e)
    #finally:
     #   print("Successful")
      #  cur.close()


#db.close()
