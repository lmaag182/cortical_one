import sys, os
# import atexit
import platform

try:
    import serial  # Python2
except ImportError:
    from serial3 import *  # Python3

from stompest.config import StompConfig
from stompest.sync import Stomp

# def exit_handler():
#     print 'My application is ending!'
#     target.close()
#     ser.close()
#
#
# atexit.register(exit_handler)

print(platform.python_version())
print(os.getcwd())



CONFIG = StompConfig('tcp://localhost:61613',login='admin', passcode='password')
QUEUE = '/queue/test'
#QUEUE = '/topic/command'


#ser = serial.Serial('/dev/ttyACM0', 9600)


def do_record(number_of_records=20):
    client = Stomp(CONFIG)
    client.connect()
    ser = serial.Serial('/dev/ttyACM0', 9600)
    target = open("out.csv", 'w')
    count=0
    ser.flushInput()
    #ser.write('A')
    while count < number_of_records:
        # while True:
        count = count + 1
        text = ser.readline()
        print text
        print count
        client.send(QUEUE, text)
        if (len(text.split(",")) == 4):
            target.write(text)

    target.close()
    ser.close()
    client.disconnect()

def go():
    do_record()