import pyhop as treehop
import numpy as np
from time import sleep


def set_fov(state, cam, theta):
    preconditions = {}
    old_fov = state.fov[cam]

    def new_fov(t):
        return theta(t) + old_fov(t)

    state.fov[cam] = new_fov
    return [state], preconditions


def end_fov(state, cam, theta, time):
    preconditions = {}
    old_fov = state.fov[cam]

    def new_fov(t):
        return old_fov(t) - theta(t)

    state.fov[cam] = new_fov
    state.time['time'] += time
    return [state], preconditions


def set_angle(state, cam, theta):
    preconditions = {}
    old_angle = state.angle[cam]

    def new_angle(t):
        return theta(t) + old_angle(t)

    state.angle[cam] = new_angle
    return [state], preconditions


def end_angle(state, cam, theta, time):
    preconditions = {}
    old_angle = state.angle[cam]

    def new_angle(t):
        return old_angle(t) - theta(t)

    state.fov[cam] = new_angle
    state.time['time'] += time
    return [state], preconditions


def set_l_fov(state, cam, theta):
    preconditions = {}
    state.l_fov[cam] = theta
    return [state], preconditions


def set_r_fov(state, cam, theta):
    preconditions = {}
    state.r_fov[cam] = theta
    return [state], preconditions


def wait(state, time):
    state.time['time'] += time
    return[state], {}


treehop.declare_operators(set_l_fov, set_r_fov, wait, set_fov, set_angle)


def attach_next(state, cam):
    left, right = furthest(state)
    print(left, right)
    # left_s, right_s = largest_slopes(state)
    plan = []
    l_y = state.actors_y[left[1]]
    l_x = state.actors_x[left[1]]

    def l_t(new_time, c_time=state.time['time']):
        return np.arctan2(l_y(new_time), l_x(new_time)) - np.arctan2(l_y(c_time), l_x(c_time))

    r_y = state.actors_y[right[1]]
    r_x = state.actors_x[right[1]]

    def r_t(new_time, c_time=state.time['time']):
        return np.arctan2(r_y(new_time), r_x(new_time)) - np.arctan2(r_y(c_time), r_x(c_time))

    def d_angle(new_time):
        return (l_t(new_time) - r_t(new_time))/2

    time = state.time['time']
    if not state.left[left[1]]:
        old = [x for x in state.left if state.left[x]]
        for actor in old:
            state.left[actor] = False
        state.left[left[1]] = True
        plan.append(('set_fov', cam, l_t))
    if not state.right[right[1]]:
        old = [x for x in state.right if state.right[x]]
        for actor in old:
            state.right[actor] = False
        state.right[right[1]] = True
        plan.append(('set_fov', cam, r_t))
    wait_time = 0
    for t in range(time, time + 100):
        if wait_time > 0:
            break
        for actor in state.actors_x:
            if not actor == left[1]:
                l_y_new = state.actors_y[actor]
                l_x_new = state.actors_x[actor]
                theta = l_t(t)
                new_theta = np.arctan2(l_y_new(t), l_x_new(t))
                if new_theta < theta:
                    wait_time = t - time
                    print("left", time, t, actor, left[1], new_theta, theta)
                    break
            if not actor == right[1]:
                r_y_new = state.actors_y[actor]
                r_x_new = state.actors_x[actor]
                theta = r_t(t)
                new_theta = np.arctan2(r_y_new(t), r_x_new(t))
                if new_theta > theta:
                    print("right", time, t, actor, right[1], new_theta, theta)
                    wait_time = t - time
                    # print(time, t)
                    break
    if wait_time > 0:
        plan.append(("wait", wait_time))
        plan.append(("achieve_goal", cam))
    print(plan)
    return plan

def achieve_goal(state, cam):
    left, right = furthest(state)
    print(left, right)
    # left_s, right_s = largest_slopes(state)
    plan = []
    l_y = state.actors_y[left[1]]
    l_x = state.actors_x[left[1]]
    l_t = np.arctan2(l_y(0), l_x(0))

    r_y = state.actors_y[right[1]]
    r_x = state.actors_x[right[1]]
    r_t = np.arctan2(r_y(0), r_x(0))

    d_t = (l_t - r_t)

    def fov(t, val=d_t):
        return val

    def angle(t, val=right[0]+(d_t/2)):
        return val

    print(fov(10), angle(10))
    plan.append(('set_fov', cam, fov))
    plan.append(('set_angle', cam, angle))
    plan.append(('attach_next', state, cam))
    return plan


def furthest(state):
    left = (None, -1)
    right = (None, -1)
    t = state.time['time']
    for actor in state.actors_x:
        loc_x = state.actors_x[actor](t)
        loc_y = state.actors_y[actor](t)
        loc_t = np.arctan2(loc_y, loc_x)
        if actor != left[1]:
            if left[0] is None or loc_t > left[0]:
                left = (loc_t, actor)
        if actor != right[1]:
            if right[0] is None or loc_t < right[0]:
                right = (loc_t, actor)
    return left, right

treehop.declare_methods("achieve_goal", achieve_goal)