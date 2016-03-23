import time
import psutil
import sensor
import os

s = sensor.Sensor(
    name='cpu',
    admin_in='/topic/admin_in',
    admin_out='/topic/admin_out',
    sensor_spec=["consolidate"],
    sensors_dir='/home/hans/cortical_one_var/sensors/'
)

while True:
    values = []
    payload = psutil.cpu_percent()
    values.append(str(payload))
    print payload
    s.announcement_check()
    s.send_payload(values)
    s.check_recording(values)
    time.sleep(0.5)
