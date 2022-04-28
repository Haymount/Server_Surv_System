import RPi.GPIO as GPIO
import mfrc522 as MFRC522
import signal
import time
 
continue_reading = True

GPIO.setmode(GPIO.BCM)

LEDred = 14
GPIO.setup(LEDred, GPIO.OUT, initial=GPIO.HIGH)
LEDgreen = 18
GPIO.setup(LEDgreen, GPIO.OUT, initial=GPIO.LOW)

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
 
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
 
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
 
# Welcome message
print ("Kast med kortet bror")
print ("Press Ctrl-C to stop.")
 
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
 
    # If a card is found
    if status == MIFAREReader.MI_OK:
        print ("Card detected")
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
 
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
 
        # Print UID
        print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+','+str(uid[4]))  
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        
        #ENTER Your Card UID here           
        my_uid_brik = [231,33,64,82,212]  #brik    
        my_uid_kort = [1,179,159,46,3] #kort
        
        #Configure LED Output Pin
        #LEDred = 14
        #LEDgreen = 15
        #GPIO.setup(14, GPIO.OUT, initial=GPIO.HIGH)
        #GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)

        
        #Check to see if card UID read matches your card UID
        if uid == my_uid_brik: #or my_uid_kort:                
            print("Access Granted")
            GPIO.output(LEDgreen, GPIO.HIGH)  #Turn on LED
            time.sleep(3)                
            GPIO.output(LEDgreen, GPIO.LOW)   #Turn off LED
            
        else:                            #Don't open if UIDs don't match
            print("Access Denied - du gay XD")
            GPIO.output(LEDred, GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(LEDred, GPIO.HIGH)
        
        
##        # Authenticate
##        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
##
##        # Check if authenticated
##        if status == MIFAREReader.MI_OK:
##            MIFAREReader.MFRC522_Read(8)
##            MIFAREReader.MFRC522_StopCrypto1()
##        else:
##            print "Authentication error"