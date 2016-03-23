import sensors
import time
import psutil
import sensor
import os

#calculate sensor spec
sensors.init()
try:
    sensor_spec = []
    for chip in sensors.iter_detected_chips():
        for feature in chip:
            sensor_name = feature.label +' (' + str(chip) + ', ' + chip.adapter_name + ')'
            sensor_spec.append(sensor_name)
finally:
    sensors.cleanup()


s = sensor.Sensor(
    name='machine_data',
    admin_in='/topic/admin_in',
    admin_out='/topic/admin_out',
    sensor_spec= sensor_spec,
    sensors_dir='/home/hans/cortical_one_var/sensors/'
)

while True:

    values = []
    sensors.init()
    try:
        for chip in sensors.iter_detected_chips():
            for feature in chip:
                values.append(str( feature.get_value()))
    finally:
        sensors.cleanup()

    print ';'.join(values)
    s.sensor_check(values)

    time.sleep(0.5)