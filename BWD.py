# Domain File for Blocks World
import pyhop as treehop
import copy
from queue import *

def collect_block(state, agent, block):
    if block in state.weights and state.top[block]:
        preconditions = {'top': {block: True}}
        prev = state.acquired[agent]
        add = state.weights[block]
        state.acquired[agent] = (prev[0]+add[0], prev[1]+add[1])
        state.top[block] = False
        temp = state.on[block]
        state.top[temp] = True
        state.under[temp] = None
        old_top = [x for x in state.top_acquired if state.top_acquired[x]]
        if old_top:
            old_top = old_top[0]
            state.top_acquired[old_top] = False
            state.on[block] = old_top
            state.under[old_top] = block
        else:
            state.on[block] = None
        state.top_acquired[block] = True
        state.collected[block] = True
        return [state], preconditions
    else:
        return False


def move_block(state, agent, block):
    if state.top[block]:
        preconditions = {'top': {block: True}}
        state.top[block] = False
        temp = state.on[block]
        state.top[temp] = True
        state.on[block] = None
        state.under[temp] = None
        return [state], preconditions
    else:
        return False


treehop.declare_operators(collect_block, move_block)


def get_largest_next_type(state):
    top_list = [x for x in state.top if state.top[x]]
    largest = (None, 0)
    use_type_list = [x for x in state.weights if x in top_list]
    while not use_type_list:
        top_list = [x for x in state.under if state.under[x] in top_list]
        use_type_list = [x for x in state.weights if x in top_list]
    for block in use_type_list:
        if state.weights[block][0] > largest[1]:
            largest = (block, state.weights[block][0])
    return largest[0]


def achieve_goal(state, agent, amount):
    max_amount = amount
    moves = []
    state = copy.deepcopy(state)
    while max_amount > state.acquired[agent][0]:
        block = get_largest_next_type(state)
        temp = block
        temp_moves = []
        while not state.top[temp]:
            temp = state.under[temp]
            temp_moves.append(('move_block', agent, temp))
        temp_moves.reverse()
        for move in temp_moves:
            moves.append(move)
            move_block(state, move[1], move[2])
        moves.append(('collect_block', agent, block))
        state = collect_block(state, agent, block)[0][0]
    return moves




treehop.declare_methods('achieve_goal', achieve_goal)
