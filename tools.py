import importlib,csv

def create_init_file():
    target = open("model_0/__init__.py", 'w')
    target.close()


def getModelParamsFromName():
  create_init_file()
  importName = "model_0.model_params" #% (
    #gymName.replace(" ", "_").replace("-", "_")
  #)
  print "Importing model params from %s" % importName
  try:
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
  except ImportError:
    raise Exception("No model params exist for '%s'. Run swarm first!")
  return importedModelParams

def convert_csv():
    with open('eggs.csv', 'wb') as egg:
        eggwriter = csv.writer(egg, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        eggwriter.writerow(['s1', 's2', 's3', 's4'])
        eggwriter.writerow(['float', 'float', 'float', 'float'])
        eggwriter.writerow(['', '', '', ''])
        with open('out.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                #print ', '.join(row)
                eggwriter.writerow([row[0], row[1], row[2], row[3]])
        csvfile.close()
    egg.close()