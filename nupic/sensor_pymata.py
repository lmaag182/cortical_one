import sys
import signal
from PyMata.pymata import PyMata
import os

#analog pins
PINS = (0, 1, 2, 3)

count = 0

# Create a PyMata instance
board = PyMata("/dev/ttyACM0", verbose=True)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C')
    if board is not None:
        board.reset()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

#setup pins
for pin in PINS:
        board.set_pin_mode(pin, board.INPUT, board.ANALOG)

import time
import sensor

s = sensor.Sensor(
    name='arduino_analog',
    admin_in='/topic/admin_in',
    admin_out='/topic/admin_out',
    sensor_spec=["analog", "analog1","analog3","analog4"],
    sensors_dir='/home/hans/cortical_one_var/sensors/'
)

while True:
    values = []
    for pin in PINS:
        analog = board.analog_read(pin)
        #print analog
        values.append(str(analog))

    print ';'.join(values)

    s.announcement_check()
    s.send_payload(values)
    s.check_recording(values)
    time.sleep(0.5)