from RD import *
from random import *
import pyhop as treehop
import ContinuousExpectationsGenerator as eg
from PlotCamera import plot
from RT import run



def fov(t):
    return 0


def angle(t):
    return 0


starting_fov = fov
starting_angle = angle
state = treehop.State('state')
state.boundaries = {}
state.fov = {'cam1': starting_fov}  # at 0,0 in the coordinate system
state.angle = {'cam1': starting_angle}
state.left = {}
state.right = {}
state.actors_x = {}
state.actors_y = {}
num_actors = 5
state.time = {'time': 0}
for i in range(0, num_actors):
    slope_1 = uniform(-1, 1)
    start = uniform(-10, 10)
    state.left[i] = False
    state.right[i] = False

    def f(t, temp=start):
        return slope_1 * t + temp + 1

    state.actors_x[i] = f
    slope_2 = uniform(0, 1)

    def g(t, temp=i):
        return slope_2 * t + temp + 1

    state.actors_y[i] = g
print(state.actors_y[1], state.actors_y[2])
goals = [('achieve_goal', 'cam1')]
treehop.declare_goals(goals)
policy = treehop.pyhop_t(state, original_call=True)
eg.gen_expectations(policy)
print(state.time['time'])
run(policy, state)
