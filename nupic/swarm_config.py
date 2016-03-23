import copy

class SwarmConfig():
    def __init__(self,swarm_config_doc):
        self.swarm_config_doc = swarm_config_doc

    def get_field_names(self):
            return map(lambda x: x['fieldName'],self.swarm_config_doc['includedFields'])


    def get_column_names(self,fieldNames):
        columnNames = copy.copy(fieldNames)
        presteps = self.get_prediction_steps()
        for prediction in presteps:
            columnNames.append(self.swarm_config_doc['inferenceArgs']['predictedField']+'_predicted_' + str(prediction))
        return columnNames

    def get_prediction_steps(self):
        return self.swarm_config_doc['inferenceArgs']['predictionSteps']

    def get_predicted_field(self):
        return self.swarm_config_doc['inferenceArgs']['predictedField']
