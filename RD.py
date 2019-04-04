import pyhop as treehop
import copy
from random import *


def solve_equation(eq, time):
    eq = eq.replace("t", str(time))
    y = eval(eq)
    return y


def set_fov(state, cam):
    return


def set_angle(state, cam):
    return


def wait(state):
    return


treehop.declare_operators(set_fov, set_angle)


def achieve_goal(state):
    left = (0, -1)
    right = (0, -1)
    front = (0, -1)
    back = (0, -1)
    plan = []
    for actor in state.actors_x:
        if actor != left[1]:
            slope = (float(state.actors_x[actor].split("*")[0]))
            if slope < left[1]:
                pass
            pass
        if actor != right[1]:
            slope = (float(state.actors_x[actor].split("*")[0]))
            if slope > right[1]:
                pass
            pass
        pass
    for actor in state.actors_y:
        if actor != front[1]:
            slope = (float(state.actors_y[actor].split("*")[0]))
            if slope < front[1]:
                pass
            pass
        if actor != back[1]:
            slope = (float(state.actors_y[actor].split("*")[0]))
            if slope > back[1]:
                pass
            pass
        pass
    return plan


treehop.declare_methods("achieve_goal", achieve_goal)