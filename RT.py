from PlotCamera import plot
import pyhop
import copy
import RD


def check_func_equal(f, g):
    for i in range(0, 10000, 250):
        if not f(i) == g(i):
            return False
    return True

def check_expectations():
    return


def take_action(state, action):
    return action.children[0]


def run(policy, state):
    cam = 'cam1'
    while state in policy:
        c_time = state.time['time']
        action = policy[state]
        print(action.name[1:])
        a_time = action.name[3]
        print(a_time, c_time)
        state = take_action(state, action)
        while c_time <= a_time:
            plot(state, cam, c_time)
            c_time += 1
    return
