from AD import *


def main(n):
    state = {'clear': {}, 'floor': {}, 'on': {}}
    for i in range(10):
        state['clear'][i] = True
    goals = [('achieve_goal', n)]
    policy = treehop.pyhop_t(state, goals, True)
    print(policy)

main(10)