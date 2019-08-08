import matplotlib.pyplot as plt
import numpy as np
import math
import inspect
from time import sleep
fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')
ax.plot([0], [0], 'ro')
plt.show(block=False)
rad = 20

def plot(state, cam, c_time, wait=False):
    global ax, rad
    r = np.arange(0, rad + 1, rad)
    o = np.ones(len(r))
    ax.clear()
    angle = state.angle[cam](c_time)
    fov = state.fov[cam](c_time)
    fov_diff = fov/2
    theta = (angle - fov_diff) * o
    theta2 = (angle + fov_diff) * o
    #theta = -2*np.pi/3 * o
    #theta2 = -np.pi/3 * o
    ax.plot(theta, r)
    ax.plot(theta2, r)
    ax.set_rmax(rad)
    ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line

    for actor in state.actors_x:
        x = state.actors_x[actor](c_time)
        y = state.actors_y[actor](c_time)
        r = math.sqrt(x**2 + y**2)
        if r > rad:
            rad = r
        theta = math.atan2(y, x)
        ax.plot(theta, r, 'bx')

    xT = plt.xticks()[0]

    xL = ['0', r'$\frac{\pi}{4}$', r'$\frac{\pi}{2}$', r'$\frac{3\pi}{4}$', \
           r'$\pi$/-$\pi$', r'-$\frac{3\pi}{4}$', r'-$\frac{\pi}{2}$', r'-$\frac{\pi}{4}$']
    plt.xticks(xT, xL)
    ax.grid(True)

    ax.set_title("Radial Camera View", va='bottom')
    if wait:
        plt.pause(.1)
    return
