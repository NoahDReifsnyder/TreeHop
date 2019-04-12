import pyhop as treehop
import numpy

def solve_equation(eq, time):
    eq = eq.replace("t", str(time))
    y = eval(eq)
    return y


def set_fov(state, cam, left, right, start, end):
    return


def set_angle(state, cam, start, end):
    return


def wait(state):
    return


treehop.declare_operators(set_fov, set_angle)


def achieve_goal(state):
    left, right = furthest(state)
    left_s, right_s = largest_slopes(state)
    plan = []
    print(left, right)
    print(left_s, right_s)
    angle_l = solve_equation(state.actors_t[left[1]], state.time['time'])
    angle_r = solve_equation(state.actors_t[right[1]], state.time['time'])
    angle_l_s = state.actors_t[left[0]]
    angle_r_s = state.actors_t[right[0]]
    print(angle_l, angle_r,)
    numpy.arc
    return plan


def largest_slopes(state):
    left = (None, -1)
    right = (None, -1)
    for actor in state.actors_t:
        slope = (float(state.actors_t[actor].split("*")[0]))
        if actor != left[1]:
            if left[0] is None or slope < left[0]:
                left = (slope, actor)
        if actor != right[1]:
            if right[0] is None or slope > right[0]:
                right = (slope, actor)
    return left, right


def furthest(state):
    left = (None, -1)
    right = (None, -1)
    t = state.time['time']
    for actor in state.actors_t:
        loc_t = solve_equation(state.actors_t[actor], t)
        if actor != left[1]:
            if left[0] is None or loc_t < left[0]:
                left = (loc_t, actor)
        if actor != right[1]:
            if right[0] is None or loc_t > right[0]:
                right = (loc_t, actor)
    return left, right

treehop.declare_methods("achieve_goal", achieve_goal)