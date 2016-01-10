try:
    import serial  # Python2
except ImportError:
    from serial3 import *  # Python3

from nupic.frameworks.opf.modelfactory import ModelFactory
#from nupic.frameworks.opf.model import Model
#from tools import getModelParamsFromName

from stompest.config import StompConfig
from stompest.sync import Stomp

import os,sys

ser = serial.Serial('/dev/ttyACM0', 9600)
CONFIG = StompConfig('tcp://localhost:61613',login='admin', passcode='password')
#QUEUE = '/queue/test'
QUEUE = '/topic/command'



def get_online(number_of_records=20):# 0 means forever

    #client = Stomp(CONFIG)
    #client.connect()

    #model = ModelFactory.create(getModelParamsFromName())
    #model.enableInference({"predictedField": "s1"})
    #model.load(os.getcwd() + "/model_save")
    model = ModelFactory.loadFromCheckpoint(os.getcwd() + "/model_save")

    count=0
    ser.flushInput()
    while (count < number_of_records) or (number_of_records == 0):
        # while True:
        count = count + 1
        text = ser.readline()
        #client.send(QUEUE, text)

        #print text
        if (len(text.split(",")) == 4):
            result = model.run({
                "s1": float(text.split(",")[0]),
                "s2": float(text.split(",")[1]),
                "s3": float(text.split(",")[2]),
                "s4": float(text.split(",")[3])
            })

            #print result.rawInput


            prediction = int(result.inferences['multiStepBestPredictions'][4])
            #prediction_255 =  int(prediction * 255/1023)
            #prediction_255 =  int(prediction * 255/1023)
            sys.stdout.write("\r"+ str(prediction))
            sys.stdout.write("\t"+ text)
            #sys.stdout.write("\r"+str(prediction))
            #print "\r"+str(prediction)
            #ser.write(input + '\r\n')
            ser.write(str(prediction)+ '\n')

            #client.send('/topic/p', prediction)

