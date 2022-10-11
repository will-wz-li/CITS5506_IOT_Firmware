# Read the magnetic field strength and determine if a magnet is nearby

from PiicoDev_QMC6310 import PiicoDev_QMC6310
from PiicoDev_Unified import sleep_ms

magSensor1 = PiicoDev_QMC6310(bus=1, range=3000) # initialise the magnetometer
# magSensor.calibrate()
magSensor2 = PiicoDev_QMC6310(bus=4, range=3000) # initialise the magnetometer
magSensor3 = PiicoDev_QMC6310(bus=3, range=3000) # initialise the magnetometer

threshold =  300# microTesla or 'uT'.

def readStrength(magSensor, number):
    
    strength = magSensor.readMagnitude()   # Reads the magnetic-field strength in microTesla (uT)
    myString = number + ' : ' + str(strength) + ' uT'       # create a string with the field-strength and the unit
    print(myString)                        # Print the field strength
    
    if strength > threshold:               # Check if the magnetic field is strong
        print('Strong Magnet!')
    
while True:
    readStrength(magSensor1, '1')
    readStrength(magSensor2, '2')
    readStrength(magSensor3, '3')
    sleep_ms(1000)
