from RD import *
from random import *
import pyhop as treehop
import ContinuousExpectationsGenerator as eg
from PlotCamera import plot
import numpy as np
from time import sleep


def check_func_equal(f, g):
    for i in range(0, 10000, 250):
        if not f(i) == g(i):
            return False
    return True

def check_expectations():
    return


def take_action(state, action):
    return action.children[0]


def reverse(state, time, factor):
    for actor in state.actors_x:
        old_x = state.actors_x[actor]
        old_y = state.actors_y[actor]
        x = old_x(time)
        y = old_y(time)

        slope_1 = uniform(-1, 1)

        def f(t, temp=x, slope=slope_1):
            return slope * factor / 10 * t + temp

        state.actors_x[actor] = f
        slope_2 = uniform(0, 1)

        def g(t, temp=y, slope=slope_2):
            return slope / 10 * t + temp

        state.actors_y[actor] = g
    state.fov['cam1'] = fov
    state.angle['cam1'] = angle

    state.time['time'] = 0
    return state


def update(state, time):
    for actor in state.actors_x:
        old_x = state.actors_x[actor]
        old_y = state.actors_y[actor]
        x = old_x(time)
        y = old_y(time)

        slope_1 = uniform(-1, 1)

        def f(t, temp=x, slope=slope_1):
            return slope / 10 * t + temp

        state.actors_x[actor] = f
        slope_2 = uniform(0, 1)

        def g(t, temp=y, slope=slope_2):
            return slope / 10 * t + temp

        state.actors_y[actor] = g
    state.fov['cam1'] = fov
    state.angle['cam1'] = angle

    state.time['time'] = 0
    return state

def run(policy, state):
    cam = 'cam1'
    counter = 6
    for j in range(0, 3):
        print(j)
        while state in policy:
            c_time = state.time['time']
            counter -= 1
            action = policy[state]
            a_time = action.name[3]
            print("times", c_time, a_time, action.name[0])
            while c_time < a_time:
                print(c_time, state.fov[cam](c_time))

                plot(state, cam, c_time, True)
                c_time += 1
            state = take_action(state, action)
            plot(state, cam, c_time, True)
        t = 0
        for i in range(1, 50):
            t = state.time['time'] + i
            plot(state, cam, t, True)
        #state.angle[cam] = angle
        #state.fov[cam] = fov
        lefts = [x for x in state.left if state.left[x]]
        for x in lefts:
            state.left[x] = False
        rights = [x for x in state.right if state.right[x]]
        for x in rights:
            state.right[x] = False
        if j == 1:
            state = update(state, t)
            state = reverse(state, 0, 1)
        else:
            state = reverse(state, t, -1)
        policy = treehop.pyhop_t(state, original_call=True)
        treehop.print_policy(policy, state)
        sleep(2)
    return


def fov(t):
    return np.pi/15


def angle(t):
    return 0


def begin():
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

        def f(t, temp=start, slope=slope_1):
            return slope/10 * t + temp + 1

        state.actors_x[i] = f
        slope_2 = uniform(0, 1)

        def g(t, temp=i, slope=slope_2):
            return slope/10 * t + temp + 1

        state.actors_y[i] = g
    goals = [('achieve_goal', 'cam1')]
    treehop.declare_goals(goals)
    policy = treehop.pyhop_t(state, original_call=True)
    treehop.print_policy(policy, state)
    eg.gen_expectations(policy)
    print(state.time['time'])
    run(policy, state)


begin()
