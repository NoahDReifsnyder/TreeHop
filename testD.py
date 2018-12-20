# Grid World Domain File With Preconditions Sent To Planner
# Conformant Planning for refuelling
import pyhop as treehop
import copy
from random import *
G_eff = 10
err = .1
ND = True  # Action type


def stack(state, block1, block2):  # forward or up
    state1 = copy.copy(state)
    if state.clear[block1] and state.clear[block2] and state.energy[1][0] >= G_eff:
        preconditions = {'clear': {block1: True, block2: True}, 'energy': {1: (10, 'inf')}}
        state.on[block1] = block2
        state.clear[block2] = False
        state.energy[1] = (state.energy[1][0] - (G_eff + err), state.energy[1][1] - (G_eff - err))
        if ND:
            return [state, state1], preconditions,
        else:
            return [state], preconditions,
    else:
        print('stack')
        print(state.clear[block1], state.clear[block2])
        print(block1, block2)
        return False


treehop.declare_operators(stack)


def find_tallest(state):
    size = 0
    top = None
    for block in state.clear:
        temp_size = 0
        temp_top = block
        while block in state.on:
            temp_size += 1
            block = state.on[block]
        if temp_size > size:
            size = temp_size
            top = temp_top
    return size, top

        
def achieve_goal(state, n):
    size, top = find_tallest(state)
    clear = copy.deepcopy(state.clear)
    n = n-size
    moves = []
    used = []
    energy = state.energy[1][0]
    for i in range(n):
        if energy < G_eff:
            moves.append('recharge')
        block = choice([block for block in clear if clear[block] and block != top and block not in used])
        if not state.clear[block]:
            print(str(block)+" IS NOT CLEAR")
        moves.append(('stack', block, top))
        clear[top] = False
        energy -= (G_eff + err)
        top = block
        used.append(block)
    print(moves)
    return moves


treehop.declare_methods('achieve_goal', achieve_goal)
