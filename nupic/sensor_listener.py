import stomp
import json


class SensorListener(stomp.ConnectionListener):
    def __init__(self, sensor_name, topic):
        self.announcement_request = False
        self.start_recording = False
        self.stop_recording = False
        self.sensor_name = sensor_name
        self.topic = topic
        #print "opening sensor listener for %s on %s" % (self.sensor_name, self.topic)

    def on_error(self, headers, message):
        print('received an error "%s"' % message)

    def on_message(self, headers, message):
        print('sensor received a message "%s"\n' % message)
        if headers['destination'] == self.topic:


            # global announcement_request

            m = json.loads(message)
            if m['message']['type'] == 'sensor_announce':
                self.announcement_request = True
            if m['message']['type'] == 'sensor_command':
                # command =  m['message']['command']['name']
                command = m['message']['command']
                if command['name'] == 'start_recording':
                    if command['sensor'] == self.sensor_name:
                        # self.send(body='started recording', destination=ADMIN_IN)
                        print 'received start record command on sensor: ' + self.sensor_name
                        self.start_recording = True
                if command['name'] == 'stop_recording':
                    print 'received stop record command on sensor: ' + self.sensor_name
                    if command['sensor'] == self.sensor_name:
                        # self.send(body='started recording', destination=ADMIN_IN)
                        print 'received stop record command on sensor: ' + self.sensor_name
                        self.stop_recording = True
        else:
            print 'from listener' + message


    def get_announcement_request(self): 
        return self.announcement_request

    def set_announcement_request_false(self):
        self.announcement_request = False

    def get_start_recording_request(self):
        return self.start_recording

    def reset_start_recording_request(self):
        self.start_recording = False

    def get_stop_recording_request(self):
        return self.stop_recording

    def reset_stop_recording_request(self):
        self.stop_recording = False
