import matplotlib.pyplot as plt
import numpy as np
import math
import inspect
from time import sleep


def plot(state, cam, c_time):
    ax = plt.subplot(111, projection='polar')
    ax.plot([0], [0], 'ro')
    r = np.arange(0, 21, 20)
    o = np.ones(len(r))
    angle = state.angle[cam](c_time)
    fov = state.fov[cam](c_time)
    fov_diff = fov/2
    theta = (angle - fov_diff) * o
    theta2 = (angle + fov_diff) * o
    #theta = -2*np.pi/3 * o
    #theta2 = -np.pi/3 * o
    ax.plot(theta, r)
    ax.plot(theta2, r)
    ax.set_rmax(20)
    ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line

    for actor in state.actors_x:
        x = state.actors_x[actor](c_time)
        y = state.actors_y[actor](c_time)
        r = math.sqrt(x**2 + y**2)
        theta = math.atan2(y, x)
        ax.plot(theta, r, 'bx')

    xT = plt.xticks()[0]

    xL = ['0', r'$\frac{\pi}{4}$', r'$\frac{\pi}{2}$', r'$\frac{3\pi}{4}$', \
           r'$\pi$/-$\pi$', r'-$\frac{3\pi}{4}$', r'-$\frac{\pi}{2}$', r'-$\frac{\pi}{4}$']
    plt.xticks(xT, xL)
    ax.grid(True)

    ax.set_title("Radial Camera View", va='bottom')
    plt.show()
    return
