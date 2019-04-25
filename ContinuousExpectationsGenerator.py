import copy
from queue import *
from pyhop import Action
import time

class Expectations(object):
    def __init__(self):
        self.informed = {}
        self.immediate = {}
        self.regression = {}
        self.goldilocks = {}

    def print(self):
        for exp in vars(self):
            print(exp, getattr(self, exp))


def o_plus(dict_a, dict_b, s, t_prime):
    new_dict = {}
    key_list = [x for x in dict_b] + [x for x in dict_a]
    key_list = set(key_list)
    for x in key_list:
        new_dict[x] = {}
        if x in dict_b and x in dict_a:
            new_keys = [y for y in dict_b[x] if y in dict_a[x]]
            new_keys_a = [y for y in dict_a[x] if y not in new_keys]
            new_keys_b = [y for y in dict_b[x] if y not in new_keys]
            for new_key in new_keys:  # point 1 in paper
                new_dict[x][new_key] = dict_a[x][new_key](t) + dict_b[x][new_key](t - t_prime)
            for new_key in new_keys_a:  # point 2 in paper
                new_dict[x][new_key] = dict_b[x][new_key]
            for new_key in new_keys_b:  # point 3 in paper
                new_dict[x][new_key] = dict_b[x][new_key]
        elif x in dict_a:  # point 2 in paper
            for key in dict_a[x]:
                new_dict[x][key] = dict_a[x][key]
        elif x in dict_b:
            for key in dict_b[x]:  # point 3 in paper
                new_dict[x][key] = dict_b[x][key]
    return new_dict


def o_minus(dict_a, dict_b, s, t_prime):
    new_dict = {}
    keys = [x for x in dict_a if x not in dict_b]
    for x in keys:
        new_dict[x] = dict_a[x]
    keys = [x for x in dict_a if x in dict_b]
    for x in keys:
        new_dict[x] = {}
        keys_2 = [y for y in dict_a[x] if y not in dict_b[x]]
        for y in keys_2:
            new_dict[x][y] = dict_a[x][y]
    return new_dict


def gen_expectations(policy):
    return
