import importlib,csv, pickle
import os

def create_init_file():
    target = open("working/model_0/__init__.py", 'w')
    target.close()

def getModelParamsFromFile():
    pickle_load = open("working/model_params.pkl", 'rb')
    o = pickle.load(pickle_load)
    return o


def getModelParamsFromFileNG(config_file_path):
    pickle_load = open(config_file_path+ "model_params.pkl", 'rb')
    o = pickle.load(pickle_load)
    return o

def getModelParamsFromName():
  create_init_file()
  importName = "working.model_0.model_params" #% (
    #gymName.replace(" ", "_").replace("-", "_")
  #)
  print "Importing model params from %s" % importName
  try:
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
  except ImportError:
    raise Exception("No model params exist for '%s'. Run swarm first!")
  return importedModelParams

def convert_csv():
    with open('working/eggs.csv', 'wb') as egg:
        eggwriter = csv.writer(egg, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        eggwriter.writerow(['s1', 's2', 's3', 's4'])
        eggwriter.writerow(['float', 'float', 'float', 'float'])
        eggwriter.writerow(['', '', '', ''])
        with open('nupic/out.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                #print ', '.join(row)
                eggwriter.writerow([row[0], row[1], row[2], row[3]])
        csvfile.close()
    egg.close()

def convert_csv(filename):
    with open('working/eggs.csv', 'wb') as egg:
        eggwriter = csv.writer(egg, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        eggwriter.writerow(['s1', 's2', 's3', 's4'])
        eggwriter.writerow(['float', 'float', 'float', 'float'])
        eggwriter.writerow(['', '', '', ''])
        with open('sensors/sensor1/' + filename , 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                #print ', '.join(row)
                eggwriter.writerow([row[0], row[1], row[2], row[3]])
        csvfile.close()
    egg.close()


def prepare_swarm(field_names,field_types, egg_file, store_file):
    with open(egg_file, 'wb') as egg:
        eggwriter = csv.writer(egg, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        eggwriter.writerow(field_names)
        eggwriter.writerow(field_types)
        haha = None
        if len(field_names) == 1:
            haha = ''
        else:
            haha = ['']*len(field_names)
        eggwriter.writerow(haha)
        with open(store_file , 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                eggwriter.writerow(row)
        csvfile.close()
    egg.close()

def next_file_name(prefix, suffix, path):
    num = 1
    while True:
        filename = path + '/' + prefix + '_'+str(num) + suffix
        if not os.path.exists(filename):
            return filename
        num += 1