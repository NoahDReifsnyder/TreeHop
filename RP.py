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
state.actors_t = {}
state.actors_r = {}
num_actors = 3
state.time = {'time': 0}
for i in range(0, num_actors):
    slope = uniform(-1, 1)
    eq = str(slope) + "*t+" + str(i+1)
    solve_equation(eq, 1)
    state.actors_r[i] = eq
print(state.actors_t)
plan = achieve_goal(state)
print(plan)
