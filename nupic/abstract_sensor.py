from sensor import Sensor
import json
from nupic.frameworks.opf.modelfactory import ModelFactory
from tools import getModelParamsFromFileNG
import os
import time
import psutil
import copy
from abstract_sensor_listener import AbstractSensorListener
from swarm_config import SwarmConfig
import stomp
import threading

class AbstractSensor(Sensor, threading.Thread):
    def __init__(self,name,admin_in,admin_out,sensor_spec, sensors_dir,sensor_in,store,swarm):
        threading.Thread.__init__(self)
        #self.config = config
        self.sensor_in = sensor_in
        self.store = store
        self.swarm = swarm
        self.name = name
        self.brain_available = False
        threading.Thread.__init__(self)
        Sensor. __init__(self,name=name,admin_in=admin_in, admin_out=admin_out,sensor_spec=sensor_spec, sensors_dir=sensors_dir)
        swarm_config_path = sensors_dir  + sensor_in +'/stores/' + store + '/swarms/' + swarm +'/'
        #store_path = sensors_dir  + sensor_in +'/stores/' + store + '/out.csv'
        #model = ModelFactory.loadFromCheckpoint('/home/hans/cortical_one_var/sensors/cpu/stores/store_3/swarms/swarm_1/model_save')

        print swarm_config_path

        #load original swarm config file
        with open(swarm_config_path + 'swarm_config.json')as json_file:
            self.swarm_config = json.load(json_file)
            print(self.swarm_config)

        self.swarm_config_ng = SwarmConfig(self.swarm_config)

        print self.swarm_config_ng.get_predicted_field()


        #if there is a 'brain', then tae the existing brain
        self.possible_brain_path = str(swarm_config_path +  'model_save')
        if os.path.exists(self.possible_brain_path):
            possible_brain_2 = '/home/hans/cortical_one_var/sensors/cpu/stores/store_3/swarms/swarm_1/model_save'
            print "load existing brain..."
            print self.possible_brain_path
            #model = ModelFactory.loadFromCheckpoint(possible_brain_2)
            model = ModelFactory.loadFromCheckpoint(self.possible_brain_path)
            #use this case to add the availabilty of a 'brain' (???!!!) to your annuncement

        else:

            #laod model configuration
            model = ModelFactory.create(getModelParamsFromFileNG(swarm_config_path))

            #configure prediction
            model.enableInference({"predictedField": self.swarm_config_ng.get_predicted_field()})

        self.connection_sensor_in = stomp.Connection()
        self.connection_sensor_in.set_listener(name=self.name, lstnr=AbstractSensorListener(self.name,topic = '/topic/' +self.sensor_in,config=self.swarm_config_ng,model=model))
        self.connection_sensor_in.start()
        self.connection_sensor_in.connect(self.user, self.password, wait=True)
        #self.connection_sensor_in.connect('admin', 'password', wait=True)
        self.abstract_listener = self.connection_sensor_in.get_listener(name=self.name)
        self.connection_sensor_in.subscribe(destination='/topic/' +self.sensor_in, id=2, ack='auto')

        self.values = []

        self.self_announcement()


    def run(self):

        while True:

            self.announcement_check()
            values = self.abstract_listener.check_input()
            self.send_payload(values)
            self.check_recording(values)
            time.sleep(0.5)

    def self_announcement(self):
        stores = []
        if not os.path.exists(self.sensor_data_dir):
            os.makedirs(self.sensor_data_dir)
        store_dirs = os.listdir(self.sensor_data_dir)
        for store_dir_name in store_dirs:

            store = {}
            store['name']= store_dir_name

            swarms_dir = self.sensor_data_dir + '/' + store_dir_name + '/swarms/'
            if  os.path.exists(swarms_dir):
                swarm_dir_names = os.listdir(self.sensor_data_dir + '/' + store_dir_name + '/swarms/' )
                print store_dir_name
                swarms = []
                for swarm_dir_name in swarm_dir_names:
                    if os.path.exists(self.sensor_data_dir + '/' + store_dir_name + '/swarms/'+swarm_dir_name + '/model_save/'):
                        print "jajajajajaaaaaaaaaa..........................................."
                        #use this case to add the availabilty of a 'brain' (???!!!) to your annuncement
                    swarms.append(swarm_dir_name)
                    print '\t%s' % swarm_dir_name
                store['swarms']= swarms

            stores.append(store)

        announce = {'message': {'type': "sensor_announcement",
                                'sensor': {'name': self.name, 'sensor_items': self.swarm_config_ng.get_column_names(self.swarm_config_ng.get_field_names()),
                                           'stores':  store_dirs,
                                           'store_ng': stores
                                           }
                                }
                    }

        self.connection.send(body=json.dumps(announce), destination=self.admin_in)


