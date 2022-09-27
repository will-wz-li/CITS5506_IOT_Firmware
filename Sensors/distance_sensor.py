import RPi.GPIO as GPIO
import time


#set up 
GPIO.setmode(GPIO.BOARD)

PIN_TRIGGER = 7
PIN_ECHO = 11

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

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
    except KeyboardInterrupt:
        print("Stopped")
        GPIO.cleanup()
    
