from RD import *
from random import *
import pyhop as treehop

starting_l_fov = 0
starting_r_fov = 0
state = treehop.State('state')
state.boundaries = {}
state.l_fov = {'cam1': starting_l_fov}  # at 0,0 in the coordinate system
state.r_fov = {'cam1': starting_r_fov}
state.actors_x = {}
state.actors_y = {}
num_actors = 3
state.time = {'time': 0}
for i in range(0, num_actors):
    slope_1 = uniform(-1, 1)

    def f(t, temp=i):
        return slope_1 * t + temp + 1
    state.actors_x[i] = f
    slope_2 = uniform(0, 1)

    def g(t, temp=i):
        return slope_2 * t + temp + 1
    state.actors_y[i] = g
print(state.actors_y[1], state.actors_y[2])
plan = achieve_goal(state, 'cam1')
goals = [('achieve_goal', 'cam1')]
treehop.declare_goals(goals)
policy = treehop.pyhop_t(state, original_call=True)
print(policy)