# Read the magnetic field strength and determine if a magnet is nearby

from PiicoDev_QMC6310 import PiicoDev_QMC6310
from PiicoDev_Unified import sleep_ms

import RPi.GPIO as GPIO
import time

from datetime import datetime
import sys

#set up 
################ Ultrasonic
GPIO.setmode(GPIO.BCM)

PIN_TRIGGER = 4
PIN_ECHO = 17

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

#file_object = open(f'Data_{identifier}.txt', 'a')

############### LED
PIN_LED = 27
GPIO.setup(PIN_LED, GPIO.OUT)

    
def magneto():

    strength = magSensor.readMagnitude()   # Reads the magnetic-field strength in microTesla (uT)

    
    if strength > threshold:               # Check if the magnetic field is strong
        print('Strong Magnet!')

    sleep_ms(1000)
    return strength
    
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

def init_sensor(mag_baseline):
    # find the baseline readings for magnetometer
    # when the park space is unoccupied
    mag_baseline = magneto()
    
    

def check_parking_spot():
    # obtain 3 measurements with 10s interval, compute average
    # conditions of an occupied space:
    # - distance < 1m
    # - magnetic field increase > 20% of baseline
    occupied = 0 
    # 1
    dist = distance()
    mag = magneto()
    time.sleep(5)
    # 2
    dist += distance()
    mag += magneto()
    time.sleep(5)
    # 3
    dist += distance()
    mag += magneto()
    # average reading
    dist = dist/3
    msg = ("Distance:" + str(dist) + "cm")
    print(msg)
    
    mag = mag/3
    myString = str(mag) + ' uT'       # create a string with the field-strength and the unit
    print(myString)                        # Print the field strength
    
    if (dist < 100): #100cm = 1m
        print(mag_baseline)
        if (mag/mag_baseline > 1.2):
           occupied = 1
    
        
    return occupied

    
if __name__ == '__main__':
    
    try:
        mag_baseline = magneto()
        
        while True:
            occupied = check_parking_spot()
            GPIO.output(PIN_LED, occupied)
            
            date = datetime.now()
            #file_object.write(str(dist) + " " + str(mag) + " "+
            #                str(date)+ "\n")
    except KeyboardInterrupt:
        print("Stopped")
        GPIO.cleanup()
        #file_object.close()
    
