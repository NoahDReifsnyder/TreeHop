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
    counter = 6
    while state in policy:
        c_time = state.time['time']
        counter -= 1
        action = policy[state]
        a_time = action.name[3]
        print("times", c_time, a_time, action.name[0])
        while c_time < a_time:
            print(c_time, state.fov[cam](c_time))

            plot(state, cam, c_time)
            c_time += 1
        state = take_action(state, action)
        plot(state, cam, c_time)
    return
