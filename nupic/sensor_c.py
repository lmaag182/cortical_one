import time
from sensor import Sensor
import random
import os

s = Sensor(
    name='sensor_c',
    admin_in='/topic/admin_in',
    admin_out='/topic/admin_out',
    sensor_spec=["pol2", "pol3","f3d"],
    sensors_dir='/home/hans/cortical_one_var/sensors/'
)

while True:
    values = []

    # sending random values
    a_number = 22 * random.random()
    b_number = 13 * random.random()
    c_number = 43 * random.random()
    values.append(str(a_number))
    values.append(str(b_number))
    values.append(str(c_number))
    payload = str(a_number)+';'+ str(b_number) +';'+ str(c_number)
    s.sensor_check(values)
    print payload
    time.sleep(0.5)