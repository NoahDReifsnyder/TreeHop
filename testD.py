# Grid World Domain File With Preconditions Sent To Planner
# Conformant Planning for refuelling
import pyhop as treehop
import copy
from random import *
G_eff = 10
err = .1
ND = True  # Action type


def move(state):
    precond = {}
    return [state], precond


def achieve_goal(state):
    actions = []
    return actions
