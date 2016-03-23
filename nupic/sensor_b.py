import time
import psutil
import sensor
import os

s = sensor.Sensor(
    name='sensor_b',
    admin_in='/topic/admin_in',
    admin_out='/topic/admin_out',
    sensor_spec=["cpu1", "claudia","roger"],
    sensors_dir='/home/hans/cortical_one_var/sensors/'
)

while True:
    values = ['88','13','45']

    # sending random values
    yo = psutil.cpu_percent(percpu=True)
    for value in yo:
        print value

    s.sensor_check(values)
    print values
    time.sleep(0.5)