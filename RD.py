import pyhop as treehop
import numpy as np
from PlotCamera import plot
import inspect
l_s = (0, None, None)
r_s = (0, None, None)


def init_fov(state, cam, theta, s_time):
    preconditions = {}
    old_fov = state.fov[cam]

    def new_fov(t):
        return old_fov(t) + theta(t)

    state.fov[cam] = new_fov
    return [state], preconditions


def init_angle(state, cam, theta, s_time):
    preconditions = {}
    old_angle = state.angle[cam]

    def new_angle(t):
        return old_angle(t) + theta(t)

    state.angle[cam] = new_angle
    return [state], preconditions


def set_fov(state, cam, theta, s_time):
    preconditions = {}
    old_fov = state.fov[cam]

    def new_fov(t):
        return old_fov(t) + theta(t)

    state.fov[cam] = new_fov
    return [state], preconditions


def end_fov(state, cam, theta, e_time, diff):
    preconditions = {}
    old_fov = state.fov[cam]
    s_time = e_time - diff
    print(theta, l_s, r_s)
    def new_fov(t):
        return old_fov(t) - theta(t) + theta(e_time)

    state.fov[cam] = new_fov
    state.time['time'] = e_time
    return [state], preconditions


def set_angle(state, cam, theta, s_time):
    preconditions = {}
    old_angle = state.angle[cam]

    def new_angle(t):
        return old_angle(t) + theta(t)

    state.angle[cam] = new_angle
    return [state], preconditions


def end_angle(state, cam, theta, e_time, diff):
    preconditions = {}
    old_angle = state.angle[cam]
    s_time = e_time - diff
    def new_angle(t):
        return old_angle(t) - theta(t) + theta(e_time)

    state.angle[cam] = new_angle
    state.time['time'] = e_time
    return [state], preconditions


def wait(state, time):
    state.time['time'] += time
    return[state], {}


treehop.declare_operators(wait, set_fov, set_angle, end_fov, end_angle, init_angle, init_fov)


def attach_next(state, cam):
    global l_s, r_s
    left, right = furthest(state)
    plan = []
    time = state.time['time']
    l_y = state.actors_y[left[1]]
    l_x = state.actors_x[left[1]]
    r_y = state.actors_y[right[1]]
    r_x = state.actors_x[right[1]]

    print('huh', time)

    def l_t(new_time):
        return np.arctan2(l_y(new_time), l_x(new_time))

    def r_t(new_time):
        return np.arctan2(r_y(new_time), r_x(new_time))

    def d_l_t(new_time, c_time=time):
        return l_t(new_time) - l_t(c_time)

    def d_l_angle(new_time, c_time=time):
        return (l_t(new_time) - l_t(c_time)) / 2

    def d_r_t(new_time, c_time=time):
        return -1 * (r_t(new_time) - r_t(c_time))

    def d_r_angle(new_time, c_time=time):
        return (r_t(new_time) - r_t(c_time)) / 2

    if not state.left[left[1]]:
        old = [x for x in state.left if state.left[x]]
        for actor in old:
            state.left[actor] = False
        state.left[left[1]] = True
        l_s = (time, d_l_t, d_l_angle)
        plan.append(('set_fov', cam, d_l_t, time))
        plan.append(('set_angle', cam, d_l_angle, time))

    if not state.right[right[1]]:
        old = [x for x in state.right if state.right[x]]
        for actor in old:
            state.right[actor] = False
        state.right[right[1]] = True
        r_s = (time, d_r_t, d_r_angle)
        plan.append(('set_fov', cam, d_r_t, time))
        plan.append(('set_angle', cam, d_r_angle, time))
    wait_time = 0
    for t in range(time, time + 100):
        if wait_time > 0:
            break
        for actor in state.actors_x:  # make this better by finding max, not first
            if not actor == left[1]:
                l_y_new = state.actors_y[actor]
                l_x_new = state.actors_x[actor]
                theta = l_t(t)
                new_theta = np.arctan2(l_y_new(t), l_x_new(t))
                if new_theta > theta:
                    wait_time = t - time

                    def diff(n_t, c_time=t):
                        return l_t(c_time) - np.arctan2(state.actors_y[actor](c_time), state.actors_x[actor](c_time))

                    print(diff(0))
                    plan.append(('end_fov', cam, l_s[1], t, wait_time))
                    plan.append(('end_angle', cam, l_s[2], t, wait_time))
            if not actor == right[1]:
                r_y_new = state.actors_y[actor]
                r_x_new = state.actors_x[actor]
                theta = r_t(t)
                new_theta = np.arctan2(r_y_new(t), r_x_new(t))
                if new_theta < theta:
                    wait_time = t - time
                    plan.append(('end_fov', cam, r_s[1], t, wait_time))
                    plan.append(('end_angle', cam, r_s[2], t, wait_time))
    if wait_time > 0:
        plan.append(("attach_next", cam))
    return plan


def achieve_goal(state, cam):
    left, right = furthest(state)
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

    plan.append(('init_fov', cam, fov, 0))
    plan.append(('init_angle', cam, angle, 0))
    plan.append(('attach_next', cam))
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
treehop.declare_methods("attach_next", attach_next)
