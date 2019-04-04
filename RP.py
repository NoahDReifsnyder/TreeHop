from RD import *
from random import *
from ExpectationsGenerator import *
import time

starting_fov = 90
starting_angle = 0
state = treehop.State('state')
state.boundaries = {}
state.fov = {'cam1': starting_fov}  # at 0,0 in the coordinate system
state.angle = {'cam1': starting_angle}
state.actors_x = {}
state.actors_y = {}
num_actors = 3
state.time = {'time': 0}
for i in range(0, num_actors):
    slope = uniform(-2, 2)
    eq = str(slope) + "*t+" + str(i)
    solve_equation(eq, 1)
    state.actors_x[i] = eq
    slope = uniform(-2, 2)
    eq = str(slope) + "*t+" + str(i)
    state.actors_y[i] = eq  # starting assumption, only move linearly
print(state.actors_x)
print(state.actors_y)
plan = achieve_goal(state)
print(plan)
