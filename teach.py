import csv,os
from nupic.frameworks.opf.modelfactory import ModelFactory
from tools import getModelParamsFromName


def do_teach():

    model = ModelFactory.create(getModelParamsFromName())
    model.enableInference({"predictedField": "s1"})

    target = open("teach.csv", 'w')
    spamwriter = csv.writer(target, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['s1', 's2', 's3', 's4', 'predicts1'])

    with open('out.csv', 'rb') as csvfile:

        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            print ', '.join(row)

            result = model.run({
                "s1": float(row[0]),
                "s2": float(row[1]),
                "s3": float(row[2]),
                "s4": float(row[3])
            })
            print result.rawInput
            print result.inferences['multiStepBestPredictions']

            spamwriter.writerow([float(row[0]), float(row[1]), float(row[2]), float(row[3]), result.inferences['multiStepBestPredictions'][4]])


    model.save(os.getcwd() + "/model_save")

def go():
    do_teach()
