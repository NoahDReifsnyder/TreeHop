# file to run environments for testing
import pyhop
from random import *
from ExpectationsGenerator import *
import copy
from datetime import datetime
from importlib import reload
import sys
import time
import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt
import pyhop as treehop
P = None
D = None
expectation_types = ['immediate', 'informed', 'regression', 'goldilocks']
#expectation_types = ['goldilocks']

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


def plot(data):
    data.append(action_counter)
    counter = 0;
    action_counter['title'] = "Actions"
    for d in data:
        for expectation in expectation_types:
            print(expectation)
            d_lists = sorted(d[expectation].items())
            d_x, d_y = zip(*d_lists)
            d_y = list(d_y)
            prev = 0
            for idx, val in enumerate(d_y):
                d_y[idx] = val + prev
                prev = d_y[idx]
            plt.plot(d_x, d_y, label=expectation)
        plt.legend(loc='upper left', shadow=True)
        title = d['title']+'.png'
        counter += 1
        plt.title(title)
        plt.show()
        plt.savefig(title)



def check_equality(first, second):
    if type(first) == dict:
        first = first.keys()
    else:
        first = [first]
    if type(second) == dict:
        second = second.keys()
    else:
        second = [second]
    for f in first:
        for s in second:
            if type(f) == tuple:
                if type(s) == tuple:
                    if type(f[0]) == tuple:
                        reg = True
                        inf = True
                        if f[0]:
                            f_1 = f[0]
                            reg = __ge__(s[0], f_1[0]) and __le__(s[1], f_1[1])
                        if f[1]:
                            f_2 = list(f[1].keys())[0]
                            inf = __ge__(s[0], f_2[0]) and __le__(s[1], f_2[1])
                        return reg and inf
                    else:
                        return __ge__(s[0], f[0]) and __le__(s[1], f[1])
                else:
                    return False
            else:
                return f == s


def check_expectations(state, expectations, exp_type):
    expectations = getattr(expectations, exp_type)
    for category in expectations:
        if hasattr(state, category):
            for key in expectations[category]:
                if key in getattr(state, category):
                    if not check_equality(expectations[category][key], getattr(state, category)[key]):
                        return False
                else:
                    return False
        else:
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


def add_error(expectation):
    global errors
    if expectation not in errors:
        errors[expectation] = 0
    errors[expectation] += 1


def reload_pyhop():
    pyhop.reset()


def replan(state):
    delattr(state, "expectations")
    reload_pyhop()
    P.policy = treehop.pyhop_t(state, original_call=True)
    gen_expectations(P.policy, state)
    pass


reqP = .5  # required percentage for expectations to be true
action_counter = {}  # keeps track of actions taken
errors = {}


def take_action(state, action, i, expectation):
    global counter
    if expectation not in action_counter:
        action_counter[expectation] = {}
    if i not in action_counter[expectation]:
        action_counter[expectation][i] = 0
    prev = copy.deepcopy(state)
    action_counter[expectation][i] += 1
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
