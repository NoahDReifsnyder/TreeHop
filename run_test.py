# file to run environments for testing
P = None
D = None
import pyhop
from random import *
from ExpectationsGenerator import *
import copy
from datetime import datetime
from importlib import reload
import sys
import time


def set_domain(domain):
    global P, D
    p_string=domain+'P'
    d_string=domain+'D'
    P = __import__(p_string)
    D = __import__(d_string)

def determine_value(val_range):
    ran_range = val_range[1] - val_range[0]
    ran_val = random()
    ran_val *= ran_range
    ran_val += val_range[0]
    ran_val = round(ran_val, 2)
    print(val_range, ran_val)
    retval = (ran_val, ran_val)
    return retval


def reload_pyhop():
    pyhop.verticies = []


reqP = .5  # required percentage for expectations to be true


def take_action(state):
    prev = copy.deepcopy(state)
    counter += 1
    action = policy[state]
    returnval = getattr(D, action.name[0])(state, *action.name[1:])
    state = action.children[0]
    for numeric_value in pyhop.numeric_values:
        for key in getattr(state, numeric_value):
            getattr(state, numeric_value)[key] = determine_value(getattr(state, numeric_value)[key])
counter = 0  # keeps track of actions taken
fuel_consumed = 0
countFailed = 0  # keeps track of replans
num_runs = 10
for x in range(0, num_runs):
    reload_pyhop()
    reload(P)
    state = copy.deepcopy(P.state)  # gets starting state from problem file
    policy = pyhop.pyhop_t(state, pyhop.goals, True)
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
