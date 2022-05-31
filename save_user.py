#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector

L1 = 24 #25
L2 = 18 #8
L3 = 17 #7
L4 = 1

C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Make sure to configure the input pins to use the internal pull-down resistors

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        print(characters[0])
    if(GPIO.input(C2) == 1):
        print(characters[1])
    if(GPIO.input(C3) == 1):
        print(characters[2])
    if(GPIO.input(C4) == 1):
        print(characters[3])
    GPIO.output(line, GPIO.LOW)

class keypad:
  try:
    while True:
        # call the readLine function for each row of the keypad
        readLine(L1, ["1","2","3","A"])
        readLine(L2, ["4","5","6","B"])
        readLine(L3, ["7","8","9","C"])
        readLine(L4, ["*","0","#","D"])
        time.sleep(0.1)
  except KeyboardInterrupt:
    print("\nApplication stopped!")

print("test3")
GPIO.setwarnings(False)
db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="fedtfirma42",
  database="rfiddb"
)

cursor = db.cursor()
reader = SimpleMFRC522()

try:
  while True:
   # lcd.clear()
    print('Place Card to\nregister')
    id, text = reader.read()
    get_rfid_uid = "SELECT id FROM users WHERE rfid_uid = '{}'".format(str(id))
    cursor.execute(get_rfid_uid)
    cursor.fetchone()

    if cursor.rowcount >= 1:
     # lcd.clear()
      print("Overwrite\nexisting user?")
      overwrite = input("Overwite (Y/N)? ")
      if overwrite[0] == 'Y' or overwrite[0] == 'y':
       # lcd.clear()

        print('Enter new name')
        new_name = input("Name: ")
        keypad()
        Pin = input("Indtast en 4 cifret tal kode: ")
        Pin = int(Pin)
        if Pin <= int(999):
            print("fejl maks 4 tal ")
            keypad()
            Pin = input("Indtast den her igen: ")
            Pin = int(Pin)
        elif Pin >= int(10000):
            print("Fejl maks 4 cifre")
            keypad()
            Pin = input("Indtast den her igen: ")
            Pin = int(Pin)
        print("Overwriting user.")
        Pin = int(Pin)
        time.sleep(1)
        sql_insert = "UPDATE users SET name = '{}' WHERE rfid_uid = '{}'".format(new_name,str(id))
        sql_insert2 = "UPDATE users SET Pin = '{}' WHERE rfid_uid = '{}'".format(Pin,str(id))
        cursor.execute(sql_insert)
        cursor.execute(sql_insert2)
        db.commit()
      else:
        continue;
    else:
        print('Enter new name')
        new_name = input("Name: ")
        keypad()
        Pin = input("Indtast en 4 cifret tal kode: ")
        Pin = int(Pin)
        if Pin <= 999:
            print("fejl maks 4 tal ")
            keypad()
            Pin = input("Indtast den her igen: ")
            Pin = int(Pin)
        elif Pin >= 10000:
            print("Fejl maks 4 cifre")
            keypad()
            Pin = input("Indtast den her igen: ")
            Pin = float(Pin)
        sql_insert = "INSERT INTO users (name, rfid_uid, Pin) VALUES ('{}', '{}', '{}')".format(new_name, str(id),Pin)
        cursor.execute(sql_insert)
        db.commit()


    if Pin <= 999:
      print("fejl maks 4 tal ")
      keypad()
      Pin = input("Indtast den her igen: ")
      Pin = int(Pin)
    elif Pin >= 10000:
      print("Fejl maks 4 cifre")
      Pin = input("Indtast den her igen: ")
      Pin = int(Pin)

    find_rfid_uid = "SELECT * FROM users WHERE rfid_uid = '{}'".format(str(id))
    cursor.execute(find_rfid_uid)

    #db.commit()

   # lcd.clear()
    print("User " + new_name + "\nSaved")
    time.sleep(2)
finally:
  GPIO.cleanup()