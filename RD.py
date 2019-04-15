import pyhop as treehop
import numpy as np



def set_l_fov(state, cam, theta):
    state.l_fov[cam] = theta
    return


def set_r_fov(state, cam, theta):
    state.r_fov[cam] = theta
    return


def wait(state):
    return


treehop.declare_operators(set_l_fov, set_r_fov, wait)


def achieve_goal(state, cam):
    left, right = furthest(state)
    # left_s, right_s = largest_slopes(state)
    plan = []
    print(left, right)
    l_y = state.actors_y[left[1]]
    l_x = state.actors_x[left[1]]

    def l_t(t):
        return np.arctan2(l_y(t), l_x(t))
    r_y = state.actors_y[right[1]]
    r_x = state.actors_x[right[1]]

    def r_t(t):
        return np.arctan2(r_y(t), r_x(t))
    time = state.time['time']
    if not state.l_fov[cam] == l_t:
        plan.append(('set_l_fov', cam, l_t))
    if not state.r_fov[cam] == r_t:
        plan.append(('set_r_fov', cam, r_t))
    wait_time = 0
    for t in range(0, 100):
        if wait_time > 0:
            break
        for actor in state.actors_x:
            if not actor == left[1]:
                l_y_new = state.actors_y[actor]
                l_x_new = state.actors_x[actor]
                t = l_t(t)
                new_t = np.arctan2(l_y_new(t), l_x_new(t))
                if new_t < t:
                    print(t, new_t)
                    wait_time = t
                    break
            if not actor == right[1]:
                r_y_new = state.actors_y[actor]
                r_x_new = state.actors_x[actor]
                t = r_t(t)
                new_t = np.arctan2(r_y_new(t), r_x_new(t))
                if new_t > t:
                    print(t, new_t)
                    wait_time = t
                    break
    if wait_time>0:
        plan.append(("wait", t))
        plan.append(("achieve_goal", cam))
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
    for actor in state.actors_x:
        print(actor)
        print(state.actors_x[actor](t))
        loc_x = state.actors_x[actor](t)
        loc_y = state.actors_y[actor](t)
        loc_t = np.arctan2(loc_y, loc_x)
        print(loc_x, loc_y, loc_t)
        if actor != left[1]:
            if left[0] is None or loc_t < left[0]:
                left = (loc_t, actor)
        if actor != right[1]:
            if right[0] is None or loc_t > right[0]:
                right = (loc_t, actor)
    return left, right

treehop.declare_methods("achieve_goal", achieve_goal)