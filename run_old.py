import sys, os
import platform
import atexit
import numpy
import csv
from nupic.encoders import ScalarEncoder
from nupic.research.spatial_pooler import SpatialPooler
from nupic.swarming import permutations_runner
from nupic.frameworks.opf.modelfactory import ModelFactory

try:
    import serial  # Python2
except ImportError:
    from serial3 import *  # Python3

good = False



def exit_handler():
    print 'My application is ending!'
    target.close()
    ser.close()


atexit.register(exit_handler)

print(platform.python_version())
print(os.getcwd())

target = open("out.csv", 'w')

enc = ScalarEncoder(n=35, w=7, minval=500, maxval=1023, clipInput=True, forced=True)

sp = SpatialPooler(inputDimensions=(35,),
                   columnDimensions=(20,),
                   potentialRadius=15,
                   numActiveColumnsPerInhArea=1,
                   globalInhibition=True,
                   synPermActiveInc=0.03,
                   potentialPct=1.0)

# show which coloumns are connected to the input bits without having learned anything
for column in xrange(20):
    connected = numpy.zeros((35,), dtype="int")
    sp.getConnectedSynapses(column, connected)
    print connected

output = numpy.zeros((20,), dtype="int")
sp.compute(enc.encode(float("899")), learn=True, activeArray=output)
print output

ser = serial.Serial('/dev/ttyACM0', 9600)

count = 0

#record a time series and save it to file
while count < 20:
    # while True:
    count = count + 1
    text = ser.readline()
    # if (text== "init"):
    #     good = True

    # try:
    #     text.split(",")[0]
    #     text.split(",")[1]
    #     text.split(",")[2]
    #     text.split(",")[3]
    # except ValueError, IndexError:
    #     print "bad record"
    print text
    if (len(text.split(",")) == 4):
        print "0 =", enc.encode(float(text.split(",")[0]))
        sp.compute(enc.encode(float(text.split(",")[0])), learn=True, activeArray=output)
        print "1 =", enc.encode(float(text.split(",")[1]))

        print "2 =", enc.encode(float(text.split(",")[2]))

        print "3 =", enc.encode(float(text.split(",")[3]))

        target.write(text)


        # print(".")
        # sys.stdout.write(ser.read())
        # target.write(text)
        # sys.stdout.flush()

# show which coloumns are connected to the input bits after learning
for column in xrange(20):
    connected = numpy.zeros((35,), dtype="int")
    sp.getConnectedSynapses(column, connected)
    print connected

target.close()


# ser.close()

def convert_csv():
    with open('eggs.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['s1', 's2', 's3', 's4'])
        spamwriter.writerow(['float', 'float', 'float', 'float'])
        spamwriter.writerow(['', '', '', ''])
        with open('out.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                print ', '.join(row)
                spamwriter.writerow([row[0], row[1], row[2], row[3]])


def run_swarm():
    swarm_config = {}  # complete swarm config here
    return permutations_runner.runWithJsonFile(os.getcwd() + "/search_def.json",{'maxWorkers': 8, 'overwrite': True}, "test", os.getcwd())


def run_online():
    count=0
    model = ModelFactory.create(run_swarm())
    model.enableInference({"predictedField": "s1"})
    while count < 200:
        count = count + 1
        text = ser.readline()

        result = model.run({
            "s1": float(text.split(",")[0]),
            "s2": float(text.split(",")[1]),
            "s3": float(text.split(",")[2]),
            "s4": float(text.split(",")[3])
        })
        print result.rawInput
        print result.inferences['multiStepBestPredictions']



convert_csv()

run_online()


