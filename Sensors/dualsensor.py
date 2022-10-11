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

B1_PIN_TRIGGER = 4
B1_PIN_ECHO = 14
GPIO.setup(B1_PIN_TRIGGER, GPIO.OUT)
GPIO.setup(B1_PIN_ECHO, GPIO.IN)

B2_PIN_TRIGGER = 5
B2_PIN_ECHO = 6
GPIO.setup(B2_PIN_TRIGGER, GPIO.OUT)
GPIO.setup(B2_PIN_ECHO, GPIO.IN)

B3_PIN_TRIGGER = 21
B3_PIN_ECHO = 20
GPIO.setup(B3_PIN_TRIGGER, GPIO.OUT)
GPIO.setup(B3_PIN_ECHO, GPIO.IN)

################# Mag
magSensor1 = PiicoDev_QMC6310(bus=1, range=3000) # initialise the magnetometer
# magSensor.calibrate()
magSensor2 = PiicoDev_QMC6310(bus=4, range=3000) # initialise the magnetometer
magSensor3 = PiicoDev_QMC6310(bus=3, range=3000) # initialise the magnetometer

threshold =  300# microTesla or 'uT'.

################ write to file
current_time = datetime.now()
current_time = current_time.strftime("%Y-%d-%M-%H-%M-%S")
identifier = ''.join(sys.argv[1:2])

#file_object = open(f'Data_{identifier}.txt', 'a')

############### LED
B1_LED_GREEN = 15
GPIO.setup(B1_LED_GREEN, GPIO.OUT)
B1_LED_RED = 18
GPIO.setup(B1_LED_RED, GPIO.OUT)

B2_LED_GREEN = 10
GPIO.setup(B2_LED_GREEN, GPIO.OUT)
B2_LED_RED = 9
GPIO.setup(B2_LED_RED, GPIO.OUT)

B3_LED_GREEN = 16
GPIO.setup(B3_LED_GREEN, GPIO.OUT)
B3_LED_RED = 19
GPIO.setup(B3_LED_RED, GPIO.OUT)

    
def magneto(magSensor):

    strength = magSensor.readMagnitude()   # Reads the magnetic-field strength in microTesla (uT)
    if strength > threshold:               # Check if the magnetic field is strong
        print('Strong Magnet!')

    sleep_ms(1000)
    return strength
    
def distance(PIN_TRIGGER, PIN_ECHO):    
    # init
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    #print("Waiting for sensor to settle")
    time.sleep(2)
    
    # calculate distance
    #print("Calulating distance")
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

def init_sensor(mag_baseline, sensor):
    # find the baseline readings for magnetometer
    # when the park space is unoccupied
    mag_baseline = magneto(sensor)
    
    

def check_parking_spot(magSensor,mag_baseline,PIN_TRIGGER,PIN_ECHO, number):
    # obtain 3 measurements with 10s interval, compute average
    # conditions of an occupied space:
    # - distance < 1m
    # - magnetic field increase > 20% of baseline
    occupied = False 
    # 1
    dist = distance(PIN_TRIGGER,PIN_ECHO)
    mag = magneto(magSensor)
    time.sleep(1)
    # 2
    dist += distance(PIN_TRIGGER,PIN_ECHO)
    mag += magneto(magSensor)
    time.sleep(1)
    # 3
    dist += distance(PIN_TRIGGER,PIN_ECHO)
    mag += magneto(magSensor)
    # average reading
    dist = dist/3
    msg = (number + ' : ' "Distance:" + str(dist) + "cm")
    print(msg)
    
    mag = mag/3
    myString = number + ' : ' + str(mag) + ' uT'       # create a string with the field-strength and the unit
    print(myString)                        # Print the field strength
    
    if (dist < 100): #100cm = 1m
        #print(mag_baseline)
        if (mag/mag_baseline > 1.2):
            occupied = True
    
    print('\n')    
    return occupied

def toggle_LED(occupied, LED_RED, LED_GREEN):
                
    if (occupied):
        GPIO.output(LED_RED, GPIO.HIGH)
        GPIO.output(LED_GREEN, GPIO.LOW)
    else:
        GPIO.output(LED_GREEN, GPIO.HIGH)
        GPIO.output(LED_RED, GPIO.LOW)

    
if __name__ == '__main__':
    
    try:
        
        mag1_baseline = magneto(magSensor1)
        mag2_baseline = magneto(magSensor2)
        mag3_baseline = magneto(magSensor3)
        
        
        while True:
            B1_occupied = check_parking_spot(magSensor1,mag1_baseline,B1_PIN_TRIGGER,B1_PIN_ECHO, '1')
            toggle_LED(B1_occupied, B1_LED_RED, B1_LED_GREEN)
            
            B2_occupied = check_parking_spot(magSensor2,mag2_baseline,B2_PIN_TRIGGER,B2_PIN_ECHO, '2')
            toggle_LED(B2_occupied, B2_LED_RED, B2_LED_GREEN)
            
            B3_occupied = check_parking_spot(magSensor3,mag3_baseline,B3_PIN_TRIGGER,B3_PIN_ECHO, '3')
            toggle_LED(B3_occupied, B3_LED_RED, B3_LED_GREEN)

            
            date = datetime.now()
            #file_object.write(str(dist) + " " + str(mag) + " "+
            #                str(date)+ "\n")
    except KeyboardInterrupt:
        print("Stopped")
        GPIO.cleanup()
        #file_object.close()
    
