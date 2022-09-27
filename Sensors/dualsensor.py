# Read the magnetic field strength and determine if a magnet is nearby

from PiicoDev_QMC6310 import PiicoDev_QMC6310
from PiicoDev_Unified import sleep_ms

import RPi.GPIO as GPIO
import time

from datetime import datetime
import sys

################ Ultrasonic
#set up 
GPIO.setmode(GPIO.BOARD)

PIN_TRIGGER = 7
PIN_ECHO = 11

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

################# Mag
magSensor = PiicoDev_QMC6310(range=3000) # initialise the magnetometer
# magSensor.calibrate()

threshold =  300# microTesla or 'uT'.

################ write to file
current_time = datetime.now()
current_time = current_time.strftime("%Y-%d-%M-%H-%M-%S")
identifier = ''.join(sys.argv[1:2])

file_object = open(f'Data_{identifier}.txt', 'a')
    
def magneto():

    strength = magSensor.readMagnitude()   # Reads the magnetic-field strength in microTesla (uT)
    myString = str(strength) + ' uT'       # create a string with the field-strength and the unit
    print(myString)                        # Print the field strength
    
    return strength
    
    if strength > threshold:               # Check if the magnetic field is strong
        print('Strong Magnet!')

    sleep_ms(1000)
    
def distance():    
    # init
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    print("Waiting for sensor to settle")
    time.sleep(2)
    
    # calculate distance
    print("Calulating distance")
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    
    # measure time of pulse to travel
    while GPIO.input(PIN_ECHO) == 0:
        pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO) == 1:
        pulse_end_time = time.time()
        
    # calculate distance from time and speed 
    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    return distance


    
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            msg = ("Distance:" + str(dist) + "cm")
            print(msg)
            time.sleep(1)
            
            mag = magneto()
            
            date = datetime.now()
            file_object.write(str(dist) + " " + str(mag) + " "+
                            str(date)+ "\n")
    except KeyboardInterrupt:
        print("Stopped")
        GPIO.cleanup()
        file_object.close()
    
