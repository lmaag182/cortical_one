import csv,os,copy
from nupic.frameworks.opf.modelfactory import ModelFactory
from tools import getModelParamsFromFile, getModelParamsFromFileNG
import json


def do_teach_ng(sensors_dir_ng,sensor,store,swarm):
    swarm_config_path = sensors_dir_ng  + sensor +'/stores/' + store + '/swarms/' + swarm +'/'
    store_path = sensors_dir_ng  + sensor +'/stores/' + store + '/out.csv'


    print swarm_config_path

    #load original swarm config file
    with open(swarm_config_path + 'swarm_config.json')as json_file:
        swarm_config = json.load(json_file)
        print(swarm_config)

    print swarm_config['inferenceArgs']['predictedField']

    #laod model configuration
    model = ModelFactory.create(getModelParamsFromFileNG(swarm_config_path))

    #configure prediction
    model.enableInference({"predictedField": swarm_config['inferenceArgs']['predictedField']})

    target = open(swarm_config_path+"teach.csv", 'w')
    spamwriter = csv.writer(target, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    fieldNames = map(lambda x: x['fieldName'],swarm_config['includedFields'])
    columnNames = copy.copy(fieldNames)
    presteps = swarm_config['inferenceArgs']['predictionSteps']
    for prediction in presteps:
        columnNames.append(swarm_config['inferenceArgs']['predictedField']+'_predicted_' + str(prediction))
    spamwriter.writerow(columnNames)
    with open(store_path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            print ', '.join(row)

            #prepare input for model
            run_set = {}
            for index, name in enumerate(fieldNames):
                run_set[name] = float(row[index])

            #run the model
            result = model.run(run_set)

            print result.rawInput
            print result.inferences['multiStepBestPredictions']

            #spamwriter.writerow([float(row[0]), float(row[1]), float(row[2]), float(row[3]), result.inferences['multiStepBestPredictions'][4]])
            out_row = []
            for index, name in enumerate(fieldNames):
                out_row.append(float(row[index]))
            for index, predstep in enumerate(presteps):
                out_row.append(result.inferences['multiStepBestPredictions'][predstep])
            spamwriter.writerow(out_row)


    model.save(str(swarm_config_path + "/model_save"))

def go():
    do_teach()
