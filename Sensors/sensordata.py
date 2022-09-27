from datetime import datetime
from time import sleep
from datetime import datetime
import sys

current_time = datetime.now()
current_time = current_time.strftime("%Y-%d-%M-%H-%M-%S")
identifier = ''.join(sys.argv[1:2])

#file_object = open(f'Data_{current_time}_{identifier}.txt', 'a')
file_object = open(f'Data_{identifier}.txt', 'a')
for x in range(0,50):
    sensor_data = 1
    date = datetime.now()
    file_object.write(str(sensor_data) + " " + str(date)+ "\n")
    print(str(sensor_data) + " " + str(date)+ "\n")
    sleep(0.5)
file_object.close()
