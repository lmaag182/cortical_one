from nupic.swarming import permutations_runner
from tools import convert_csv
import csv,os


def run_swarm():
    convert_csv()
    swarm_config = {}  # complete swarm config here
    return permutations_runner.runWithJsonFile(os.getcwd() + "/search_def.json",{'maxWorkers': 8, 'overwrite': True}, "test", os.getcwd())

def go():
    run_swarm()