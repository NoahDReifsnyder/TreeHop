# file to run environments for testing
P = __import__('MWP')  # substitute problem file here
D = __import__('MWD')  # substitue domain file here
from MWD import *
import pyhop
from random import *
from ExpectationsGenerator import *
import copy
from datetime import datetime
from importlib import reload
import sys
import time


def determine_value(val_range):
    fuel_range = val_range[1] - val_range[0]
    ran_val = random()
    ran_val *= fuel_range
    ran_val += val_range[0]
    ran_val = round(ran_val, 2)
    print(val_range, ran_val)
    retval = (ran_val, ran_val)
    return retval


def reload_pyhop():
    pyhop.verticies = []


agent = 'Agent1'
reqP = .5  # required percentage for expectations to be true
counter = 0  # keeps track of actions taken
fuel_consumed = 0
countFailed = 0  # keeps track of replans
num_runs = 10
for x in range(0, num_runs):
    reload_pyhop()
    reload(P)
    print(x)
    state = copy.deepcopy(P.state)  # gets starting state from problem file
    policy = treehop.pyhop_t(state, treehop.goals, True)
    gen_expectations(policy, state)
    while state in policy:
        prev = copy.deepcopy(state)
        counter += 1
        action = policy[state]
        returnval = getattr(D, action.name[0])(state, *action.name[1:])
        state = action.children[0]
        for numeric_value in pyhop.numeric_values:
            for key in getattr(state, numeric_value):
                    getattr(state, numeric_value)[key] = determine_value(getattr(state, numeric_value)[key])
    print(state.beacons)
print(counter / num_runs)
