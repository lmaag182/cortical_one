from swarm import  run_swarm_ng
from teach import  do_teach_ng
import os, time
import json
import stomp
from abstract_sensor import AbstractSensor
import threading

print(os.getcwd())
import atexit

from nupic.frameworks.opf.modelfactory import ModelFactory

# CONFIG = StompConfig('tcp://localhost:61613',login='admin', passcode='password')
# QUEUE = '/topic/some'

SENSOR_NAME = 'sensor1'
SENSOR = '/topic/' + SENSOR_NAME
ADMIN_OUT = '/topic/admin_out'
ADMIN_IN = '/topic/admin_in'
WORKING_DIR = 'working'
SENSORS_DIR = 'sensors'

dir_ng = '/home/hans/cortical_one_var/'
sensors_dir_ng = dir_ng + 'sensors/'

swarming_ng = False
teaching_ng = False
online_ng = False

session_spec = {
    "includedFields": [
        {
            "fieldName": "s1",
            "fieldType": "float"
        },
        {
            "fieldName": "s2",
            "fieldType": "float"
        },
        {
            "fieldName": "s3",
            "fieldType": "float"
        },
        {
            "fieldName": "s4",
            "fieldType": "float"
        }
    ],
    "streamDef": {
        "info": "eggs",
        "version": 1,
        "streams": [
            {
                "info": "financetest4",
                "source": "file://working/eggs.csv",
                "columns": [
                    "*"
                ]
            }
        ]
    },
    "inferenceType": "TemporalMultiStep",
    "inferenceArgs": {
        "predictionSteps": [
            4
        ],
        "predictedField": "s1"
    },
    "iterationCount": -1,
    "swarmSize": "small"
}



sensor_dir = SENSORS_DIR + '/' + SENSOR_NAME


class MyListener(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print('received an error "%s"' % message)

    def on_message(self, headers, message):
        print('run received a message "%s"\n' % message)
        global conn
        global ADMIN_IN
        global swarming_ng
        global sensor
        global store
        global swarm_config
        global teaching_ng

        global session_spec
        global m
        global online_ng

        m = json.loads(message)
        if m['message']['type'] == 'command':
            command = m['message']['command']['name']
            if command == 'get_session_spec':
                reply = {'message': {'type': "reply", 'reply': {'name': "session_config", 'config': session_spec}}}
                conn.send(body=json.dumps(reply), destination=ADMIN_IN)
        if m['message']['type'] == 'swarm_ng':
            swarm_config = m['message']['config']
            sensor = m['message']['sensor']
            store = m['message']['store']
            print "...............................run swarm"
            swarming_ng = True
        if m['message']['type'] == 'teach_ng':
            print "...............................teach_ng"
            teaching_ng = True
        if m['message']['type'] == 'online_ng':
            print "...............................online_ng"
            online_ng = True

        if m['message']['type'] == 'config':
            session_spec = m['message']['config']
            print session_spec
            print "...............................got new swarm spec"

abstract_sensors = []

conn = stomp.Connection()
conn.set_listener('', MyListener())
conn.start()
conn.connect('admin', 'password', wait=True)

conn.subscribe(destination=ADMIN_OUT, id=1, ack='auto')

def new_abstract_sensor(base_sensor_name, admin_in, admin_out,store,swarm):
    print "create abstract sensor...."
    model = ModelFactory.loadFromCheckpoint('/home/hans/cortical_one_var/sensors/cpu/stores/store_3/swarms/swarm_1/model_save')
    abstract_sensor = AbstractSensor(
        name='%s_predict' % base_sensor_name,
        admin_in= admin_in,
        admin_out=admin_out,
        sensor_spec=["consolidate"], #not needed anyway
        sensors_dir=sensors_dir_ng,
        sensor_in=base_sensor_name,
        store = store,
        swarm= swarm
    )
    abstract_sensor.start()
    print "new abstract sensor created"
    #print threading.enumerate()


#print(os.getcwd())
#time.sleep(2)
while True:

    if swarming_ng == True:
        swarming_ng = False
        swarm = run_swarm_ng(working_dir=dir_ng,sensors_dir=sensors_dir_ng, sensor=sensor, store=store, swarmconfig=swarm_config)
        print "end swarming"
        #publish swarms
        reply = {'message': {'type': "new_swarm", 'new_swarm': {'swarm': swarm , 'sensor': sensor , "store" : store}}}
        conn.send(body=json.dumps(reply), destination=ADMIN_IN)

    if teaching_ng == True:
        teaching_ng = False

        do_teach_ng(
            sensors_dir_ng=sensors_dir_ng,
            sensor =  m['message']['sensor'],
            store= m['message']['store'],
            swarm = m['message']['swarm']
        )

    if online_ng == True:
        #print "create new abstract sensor..."
        online_ng = False

        #model = ModelFactory.loadFromCheckpoint('/home/hans/cortical_one_var/sensors/cpu/stores/store_3/swarms/swarm_1/model_save')
        new_abstract_sensor(base_sensor_name=m['message']['sensor'],
                            admin_in=ADMIN_IN,
                            admin_out=ADMIN_OUT,
                            store=m['message']['store'],
                            swarm=m['message']['swarm']
                            )


    time.sleep(0.1) #some weird stuff happens on other processes when starting this script with 0.1, e.g. pyfirmata and pymata get out of sync somehow, something to do wiht serial??

def gather_swarms():
    return ''

