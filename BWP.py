# Problem File for Blocks World
from BWD import *
from random import *
from ExpectationsGenerator import *
agent = 'Agent1'
state = treehop.State('state')
state.weights = {}
treehop.declare_numeric('weights')
state.acquired = {agent: (0, 0)}
treehop.declare_numeric('acquired')
n = 100
collection_weight = 500
max_weight = 100
variance = 2
for i in range(0, n):
    temp = round((random() * (max_weight - (2 * variance))) + variance, 2)
    state.weights[i] = (temp - variance, temp + variance)
goals = [('achieve_goal', agent, collection_weight)]
treehop.declare_goals(goals)
policy = treehop.pyhop_t(state, goals, True)
treehop.print_policy(policy, state)
gen_expectations(policy, state)
