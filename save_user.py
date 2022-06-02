#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector


GPIO.setwarnings(False)

db = mysql.connector.connect(
  host="192.168.10.47",
  user="mysqldb",
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