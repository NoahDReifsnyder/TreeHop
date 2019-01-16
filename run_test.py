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


def get_fuel_level(fuel):
    fuel_range = fuel[1]-fuel[0]
    ran_fuel_level = random()
    ran_fuel_level *= fuel_range
    ran_fuel_level += fuel[0]
    ran_fuel_level = round(ran_fuel_level, 2)
    print(fuel, ran_fuel_level)
    retval = (ran_fuel_level, ran_fuel_level)
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
        fuel = state.fuel[agent]
        prev = copy.deepcopy(state)
        counter += 1
        action = policy[state]
        returnval = getattr(D, action.name[0])(state, *action.name[1:])
        state = action.children[0]
        state.fuel[agent] = get_fuel_level(fuel)
    print(state.beacons)
print(counter / num_runs)
