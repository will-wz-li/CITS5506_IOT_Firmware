from PiicoDev_QMC6310 import PiicoDev_QMC6310
from PiicoDev_Unified import sleep_ms
import RPi.GPIO as GPIO

import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)

threshold =  300# microTesla or 'uT'.
magnet_range = 3000

class Sensor():
    def __init__(self, id, magSensor, dSensor, led):
        #### Parking Bay ID
        self.id = id
        #### Distance Sensor
        self.dSensor = dSensor
        GPIO.setup(self.dSensor['PIN_TRIGGER'], GPIO.OUT)
        GPIO.setup(self.dSensor['PIN_ECHO'], GPIO.IN)
        #### Magnetometer (Static For Now)
        self.magSensor = PiicoDev_QMC6310(range=magnet_range)
        self.mag_baseline = self.init_sensor()
        ##### LED
        self.PIN_LED = led['PIN_LED']
        GPIO.setup(self.PIN_LED, GPIO.OUT)

    def getStatus(self):
        occupied = self.check_parking_spot()
        GPIO.output(self.PIN_LED, occupied)
        return occupied                

    def magneto(self):
        strength = self.magSensor.readMagnitude()   # Reads the magnetic-field strength in microTesla (uT)
        sleep_ms(1000)
        return strength
        
    def distance(self):    
        # init
        GPIO.output(self.dSensor['PIN_TRIGGER'], GPIO.LOW)
        print("Waiting for sensor to settle")
        time.sleep(2)
        
        # calculate distance
        print("Calulating distance")
        GPIO.output(self.dSensor['PIN_TRIGGER'], GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.dSensor['PIN_TRIGGER'], GPIO.LOW)
        
        # measure time of pulse to travel
        while GPIO.input(self.dSensor['PIN_ECHO']) == 0:
            pulse_start_time = time.time()
        while GPIO.input(self.dSensor['PIN_ECHO']) == 1:
            pulse_end_time = time.time()
            
        # calculate distance from time and speed 
        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        return distance

    def init_sensor(self):
        # find the baseline readings for magnetometer
        # when the park space is unoccupied
        mag_baseline = self.magneto()
        return mag_baseline
        
        
    def check_parking_spot(self):
        # obtain 3 measurements with 10s interval, compute average
        # conditions of an occupied space:
        # - distance < 1m
        # - magnetic field increase > 20% of baseline
        occupied = 0 
        # 1
        dist = self.distance()
        mag = self.magneto()
        time.sleep(5)
        # 2
        dist += self.distance()
        mag += self.magneto()
        time.sleep(5)
        # 3
        dist += self.distance()
        mag += self.magneto()
        # average reading
        dist = dist/3
        msg = ("Distance:" + str(dist) + "cm")
        print(msg)
        
        mag = mag/3
        myString = str(mag) + ' uT'       # create a string with the field-strength and the unit
        print(myString)                        # Print the field strength
        
        if (dist < 100): #100cm = 1m
            print(self.mag_baseline)
            if (mag/self.mag_baseline > 1.2):
                occupied = 1
        
        return occupied
