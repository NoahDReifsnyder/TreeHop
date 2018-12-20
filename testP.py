# Grid World Problem File
from testD import *
from random import *
from ExpectationsGenerator import *
import time


state = treehop.State('state')
state.on = {}
state.clear = {}
state.energy = {1: (100, 100)}
numBlocks = 100
towerSize = 10
chanceToStack = 10
stacked = []
for i in range(numBlocks):
    state.clear[i] = True
for i in range(numBlocks):
    rand = randint(1, 100)
    block = None
    if rand < chanceToStack:
        block = randint(0, numBlocks-1)
        if block == 0:
            start = 99
        else:
            start = block-1
        while block in stacked or block == i:
            if block == 99:
                block = 0
            elif block == start:
                block = None
                break
            else:
                block += 1
    if i == block:
        print('here')
        time.sleep(5)
    state.on[i] = block
    if block is not None:
        stacked.append(block)
        state.clear[block] = False

goals = [('achieve_goal', towerSize)]
treehop.declare_goals(goals)
policy = treehop.pyhop_t(state, goals, True)
treehop.print_policy(policy, state)
gen_expectations(policy, state)
