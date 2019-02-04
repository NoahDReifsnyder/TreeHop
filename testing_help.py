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


def __ge__(self, other):
    if type(self) == str:
        if type(other) == str:
            return round(self, 2) >= round(other, 2)  # because planner rounds weird sometimes
        else:
            if self == 'inf':
                return True
            else:
                return False
    elif type(other) == str:
        if other == 'inf':
            return False
        else:
            return True
    else:
        return round(self, 2) >= round(other, 2)


def __le__(self, other):
    if type(self) == str:
        if type(other) == str:
            return round(self, 2) <= round(other, 2)
        else:
            if self == 'inf':
                return False
            else:
                return True
    elif type(other) == str:
        if other == 'inf':
            return True
        else:
            return False
    else:
        return round(self, 2) <= round(other, 2)


def check_equality(first, second):
    if type(first) == tuple:
        if type(second) == tuple:
            return __ge__(second[0], first[0]) and __le__(second[1], first[1])
        else:
            return False
    else:
        return first == second


def check_expectations(state, expectations, exp_type):
    expectations = getattr(expectations, exp_type)
    for category in expectations:
        if hasattr(state, category):
            for key in expectations[category]:
                if key in getattr(state, category):
                    if not check_equality(expectations[category][key], getattr(state, category)[key]):
                        print(category, key)
                        print(expectations[category][key], getattr(state, category)[key])
                        return False
                else:
                    print('here1')
                    return False
        else:
            print('here2')
            return False
    return True


def set_domain(domain):
    global P, D
    p_string = domain+'P'
    d_string = domain+'D'
    P = __import__(p_string)
    D = __import__(d_string)
    P.run()


def determine_value(val_range):
    ran_range = val_range[1] - val_range[0]
    ran_val = random()
    ran_val *= ran_range
    ran_val += val_range[0]
    ran_val = round(ran_val, 2)
    retval = (ran_val, ran_val)
    return retval


def reload_pyhop():
    pyhop.reset()


reqP = .5  # required percentage for expectations to be true
counter = 0  # keeps track of actions taken


def take_action(state):
    global counter
    prev = copy.deepcopy(state)
    counter += 1
    action = P.policy[state]
    returnval = getattr(D, action.name[0])(state, *action.name[1:])
    state = action.children[0]
    for numeric_value in pyhop.numeric_values:
        for key in getattr(state, numeric_value):
            getattr(state, numeric_value)[key] = determine_value(getattr(state, numeric_value)[key])
    return state


# fuel_consumed = 0
# countFailed = 0  # keeps track of replans
# num_runs = 10
# for x in range(0, num_runs):
#     reload_pyhop()
#     reload(P)
#     state = copy.deepcopy(P.state)  # gets starting state from problem file
#     policy = pyhop.pyhop_t(state, pyhop.goals, True)
#     gen_expectations(policy, state)
#     while state in policy:
#         prev = copy.deepcopy(state)
#         counter += 1
#         action = policy[state]
#         returnval = getattr(D, action.name[0])(state, *action.name[1:])
#         state = action.children[0]
#         for numeric_value in pyhop.numeric_values:
#             for key in getattr(state, numeric_value):
#                     getattr(state, numeric_value)[key] = determine_value(getattr(state, numeric_value)[key])
#     print(state.beacons)
# print(counter / num_runs)
