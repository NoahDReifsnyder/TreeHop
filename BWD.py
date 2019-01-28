# Domain File for Blocks World
import pyhop as treehop
import copy
from queue import *

def collect_block(state, agent, block):
    if block in state.weights:
        preconditions = {'weights': {block: ('-inf', 'inf')}}
        prev = state.acquired[agent]
        add = state.weights[block]
        state.acquired[agent] = (prev[0]+add[0], prev[1]+add[1])
        del state.weights[block]
        return [state], preconditions
    else:
        return False


treehop.declare_operators(collect_block)

type_list = Queue()
type_list.put(1)
type_list.put(2)
type_list.put(3)

def get_largest_next_type(state, max_val):
    largest = (None, 0)
    use_type = type_list.get()
    type_list.put(use_type)
    use_type_list = [x for x in state.weights if state.types[x] == use_type]
    for block in use_type_list:
        if max_val > state.weights[block][0] > largest[1]:
            largest = (block, state.weights[block][0])
    return largest[0]


def achieve_goal(state, agent, amount):
    max_amount = amount
    moves = []
    state = copy.deepcopy(state)
    while amount > 0:
        block = get_largest_next_type(state, amount)
        moves.append(('collect_block', agent, block))
        state = collect_block(state, agent, block)[0][0]
        amount = max_amount - state.acquired[agent][1]
    return moves


treehop.declare_methods('achieve_goal', achieve_goal)
