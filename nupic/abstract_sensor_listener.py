import stomp
import json


class AbstractSensorListener(stomp.ConnectionListener):
    def __init__(self, sensor_name, topic, config, model):
        pass
        self.sensor_name = sensor_name
        self.config = config
        self.model = model
        # self.announcement_request = False
        # self.start_recording = False
        # self.stop_recording = False
        # self.sensor_name = sensor_name
        self.topic = topic
        self.new_data = False
        self.out_row = []
        print "opening abstract sensor listener for %s on %s" % (self.sensor_name, self.topic)

    def on_error(self, headers, message):
        print('received an error "%s"' % message)

    def on_message(self, headers, message):
        self.new_data = True
        if headers['destination'] == self.topic:

            print('abstract sensor received a message "%s"' % message)
            my_list = message.split(";")
            #print('----------------my_list"%s"' % my_list)

            values = my_list

            #print '; '.join(values)

            #prepare input for model
            run_set = {}
            for index, name in enumerate(self.config.get_field_names()):
                run_set[name] = float(values[index])

            #run the model
            result = self.model.run(run_set)

            #print result.rawInput
            #print result.inferences['multiStepBestPredictions']



            self.out_row = []
            for index, name in enumerate(self.config.get_field_names()):
                self.out_row.append(str(values[index]))
            for index, predstep in enumerate(self.config.get_prediction_steps()):
                self.out_row.append(str(result.inferences['multiStepBestPredictions'][predstep]))



            #self.sensor_check(out_row)
            # # global announcement_request
            #
            # m = json.loads(message)
            # if m['message']['type'] == 'sensor_announce':
            #     self.announcement_request = True
            # if m['message']['type'] == 'sensor_command':
            #     # command =  m['message']['command']['name']
            #     command = m['message']['command']
            #     if command['name'] == 'start_recording':
            #         print 'received start record command on sensor: ' + self.sensor_name
            #         if command['sensor'] == self.sensor_name:
            #             # self.send(body='started recording', destination=ADMIN_IN)
            #             print 'received start record command on sensor: ' + self.sensor_name
            #             self.start_recording = True
            #     if command['name'] == 'stop_recording':
            #         print 'received stop record command on sensor: ' + self.sensor_name
            #         if command['sensor'] == self.sensor_name:
            #             # self.send(body='started recording', destination=ADMIN_IN)
            #             print 'received stop record command on sensor: ' + self.sensor_name
            #             self.stop_recording = True
        else:
            print 'from ddffdfdfdfdfdlistener' + message


    def check_input(self):
        #if self.new_data:
        return self.out_row

    # def get_announcement_request(self):
    #     return self.announcement_request
    #
    # def set_announcement_request_false(self):
    #     self.announcement_request = False
    #
    # def get_start_recording_request(self):
    #     return self.start_recording
    #
    # def reset_start_recording_request(self):
    #     self.start_recording = False
    #
    # def get_stop_recording_request(self):
    #     return self.stop_recording
    #
    # def reset_stop_recording_request(self):
    #     self.stop_recording = False
