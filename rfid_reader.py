import RPi.GPIO as GPIO
import mfrc522 as MFRC522
import signal
import time
import MySQLdb
import mysql.connector
from time import gmtime, strftime
from datetime import date
from mfrc522 import SimpleMFRC522
from RPLCD import *
from time import sleep
from RPLCD.i2c import CharLCD
from datetime import datetime
from py2flowchart import *

lcd = CharLCD('PCF8574', 0x27)

continue_reading = True

db = mysql.connector.connect(
  host="192.168.10.47",
  user="mysqldb",
  passwd="fedtfirma42",
  database="rfiddb"
  )

cursor = db.cursor()
cursor = db.cursor(buffered=True)
# these GPIO pins are connected to the keypad
L1 = 18 #25
L2 = 12 #8
L3 = 11 #7
L4 = 26

C1 = 32
C2 = 36
C3 = 38
C4 = 40

# Initialize the GPIO pins

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(L1, True)
GPIO.output(L2, True)
GPIO.output(L3, True)
GPIO.output(L4, True)

# Configure PIN's right

GPIO.input(C1)
GPIO.input(C2)
GPIO.input(C3)
GPIO.input(C4)

LEDred = 8
GPIO.setup(LEDred, GPIO.OUT, initial=GPIO.HIGH)
LEDgreen = 10
GPIO.setup(LEDgreen, GPIO.OUT, initial=GPIO.LOW)

i = 0
pincodeString = ""

def pincode():
  global i
  global pincodeString
  i = 0
  pincodeString = ""
  
  def readLine(line, characters):
    global i
    global pincodeString
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        pincodeString += characters[0]
        lcd.cursor_pos = (1, i)
        lcd.write_string("*")
        i += 1
        sleep(.2)
    if(GPIO.input(C2) == 1):
        pincodeString += characters[1]
        lcd.cursor_pos = (1, i)
        lcd.write_string("*")
        i += 1
        sleep(.2)
    if(GPIO.input(C3) == 1):
        pincodeString += characters[2]
        lcd.cursor_pos = (1, i)
        lcd.write_string("*")
        i += 1
        sleep(.2)
    if(GPIO.input(C4) == 1):
        pincodeString += characters[3]
        lcd.cursor_pos = (1, i)
        lcd.write_string("*")
        i += 1
        sleep(.2)
    GPIO.output(line, GPIO.LOW)
    
  while i < 4:
    readLine(L1, ["1","2","3","A"])
    readLine(L2, ["4","5","6","B"])
    readLine(L3, ["7","8","9","C"])
    readLine(L4, ["*","0","#","D"])
    sleep(0.1)
  return pincodeString


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

reader = SimpleMFRC522()


try:
  while True:
    
    # Welcome message
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('Please Scan Card')

    cardid, text = reader.read()
    
    cursor.execute("SELECT id, name, Pin, allowed_from, \
      allowed_to FROM rfid_users WHERE rfid_uid LIKE '{}'".format(str(cardid)))
    result = cursor.fetchone()
    
    if cursor.rowcount >= 1:
      
      time = datetime.now()-datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
      
      lcd.clear()
      lcd.curosor_pos = (0, 1)
      print("Enter Pincode: ")
      lcd.write_string("Enter Pincode:")
      lcd.cursor_pos = (1, 1)
      print(result)
      if time > result[3] and time < result[4]:
        Pin = pincode()
        print(Pin)
        if str(Pin) == result[2]:
          lcd.clear()
          print("Welcome " + result[1])
          lcd.cursor_pos = (0, 0)
          lcd.write_string("Welcome:")
          lcd.cursor_pos = (1,0)
          lcd.write_string(result[1])
          cursor.execute("INSERT INTO rfid_attendance (user_id, picture) VALUES (%s, %s)", \
                         (result[0],"https://i.imgur.com/K7cngYB.png"))
          db.commit()
        else:
          lcd.clear()
          lcd.cursor_pos = (0,0)
          lcd.write_string("WRONG PINCODE!")
      else:
        lcd.clear()
        lcd.cursor_pos = (0,0)
        lcd.write_string("Out of your allowed access times")
      
    else:
      print("User does not exist.")
      lcd.clear()
      lcd.cursor_pos = (0, 0)
      lcd.write_string('Access Denied')
      sleep(1)
      lcd.clear()
      lcd.cursor_pos = (1, 0)
      lcd.write_string(str(cardid))
      print(str(cardid))
      sleep(1)
    sleep(1)
finally:
  GPIO.cleanup()
  cursor.close()
  db.close()