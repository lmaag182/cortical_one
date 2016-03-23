from sensor_listener import SensorListener
from tools import next_file_name
import stomp
import json
import os


class Sensor():
    def __init__(self, name, admin_in, admin_out, sensor_spec, sensors_dir, user='admin', password='password',
                 recording=False):
        self.name = name
        self.admin_in = admin_in
        self.admin_out = admin_out
        self.user = user
        self.password = password
        self.connection = stomp.Connection()
        # self.connection.set_listener(self.name, SensorListener())
        self.connection.set_listener(name=self.name, lstnr=SensorListener(self.name, topic=self.admin_out))
        self.connection.start()
        self.connection.connect(self.user, self.password, wait=True)
        self.connection.subscribe(destination=self.admin_out, id=1, ack='auto')
        self.listener = self.connection.get_listener(self.name)
        self.sensor_spec = sensor_spec
        self.recording = recording
        self.sensors_dir = sensors_dir
        self.sensor_dir = self.sensors_dir + self.name
        self.sensor_data_dir = self.sensor_dir + '/stores'
        self.target = None
        self.next_store_dir=''
        self.new_store_name=''
        #do this only if it is a concrete sensor, that means if the code is not called by a subclass

        if self.__class__.__name__  == 'Sensor':
            self.self_announcement()
            #print '..............'+self.__class__.__name__
        #print '..............'+self.name

    # def set_sensor_spec(self, sensor_spec):
    #     self.sensor_spec = sensor_spec



    def get_listener(self):
        return self.listener



    def get_connection(self):
        return self.connection

    def announcement_check(self):
        # sensor announcement
        if self.listener.get_announcement_request():
            self.listener.set_announcement_request_false()
            self.self_announcement()


    def sensor_check(self,values):
        self.announcement_check()
        self.check_recording(values)
        self.send_payload(values)

    def check_recording(self, values):
        #print "check recording on %s" % self.name

        if not os.path.exists(self.sensor_data_dir):
            os.makedirs(self.sensor_data_dir)

        if self.listener.get_start_recording_request() and not self.recording:#check whether it is already recouding
            self.listener.reset_start_recording_request()
            self.recording = True
            print 'start recording.......'
            self.next_store_dir = next_file_name(prefix='store', suffix='', path=self.sensor_data_dir)
            path,self.new_store_name = os.path.split(self.next_store_dir)

            if not os.path.exists(self.next_store_dir):
                os.makedirs(self.next_store_dir)
            self.target = open(self.next_store_dir + '/out.csv', 'w')

        if self.listener.get_stop_recording_request():
            self.listener.reset_stop_recording_request()
            self.recording = False
            self.target.close()
            self.announce_new_record()

            #self.send_payload(payload=';'.join(payload))

        if self.recording:
            print "recording...."
            print(self.sensors_dir + self.name)
            self.target.write(','.join(values) + '\n')

    def send_payload(self, payload):
        #pass
        self.connection.send(body=';'.join(payload),destination='/topic/' + self.name)

    def self_announcement(self):
        stores = []
        if not os.path.exists(self.sensor_data_dir):
            os.makedirs(self.sensor_data_dir)
        store_dirs = os.listdir(self.sensor_data_dir)
        for store_dir_name in store_dirs:

            for i,sensor_item in enumerate(self.sensor_spec):
                self.sensor_spec[i]  =''.join(e for e in sensor_item if e.isalnum())
            store = {}
            store['name'] = store_dir_name

            swarms_dir = self.sensor_data_dir + '/' + store_dir_name + '/swarms/'
            if os.path.exists(swarms_dir):
                swarm_dir_names = os.listdir(self.sensor_data_dir + '/' + store_dir_name + '/swarms/')
                print store_dir_name
                swarms = []
                for swarm_dir_name in swarm_dir_names:
                    if os.path.exists(self.sensor_data_dir + '/' + store_dir_name + '/swarms/'+swarm_dir_name + '/model_save/'):
                        print "jajajajajaaaaaaaaaa..........................................."
                        #use this case to add the availabilty of a 'brain' (???!!!) to your annuncement

                    swarms.append(swarm_dir_name)
                    print '\t%s' % swarm_dir_name
                store['swarms'] = swarms

            stores.append(store)

        announce = {'message': {'type': "sensor_announcement",
                                'sensor': {'name': self.name, 'sensor_items': self.sensor_spec,
                                           'stores': store_dirs,
                                           'store_ng': stores
                                           }
                                }
                    }
        self.connection.send(body=json.dumps(announce), destination=self.admin_in)

    def announce_new_record(self):
        announce = {'message': {'type': "new_store", 'new_store': {'sensor': self.name , 'store': self.new_store_name}}}
        self.connection.send(body=json.dumps(announce), destination=self.admin_in)