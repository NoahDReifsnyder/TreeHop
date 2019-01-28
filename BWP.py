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
state.types = {}
state.under = {}
state.on = {}
state.top = {}
top_list = Queue()
for i in range(0, 3):
    top_list.put(None)
type_list = [1, 2, 3]
n = 200
collection_weight = 500
max_weight = 100
variance = 2
for i in range(0, n):
    under = top_list.get()
    state.under[under] = i
    state.on[i] = under
    top_list.put(i)
    temp = round((random() * (max_weight - (2 * variance))) + variance, 2)
    state.weights[i] = (temp - variance, temp + variance)
    state.types[i] = choice(type_list)
    state.top[i] = False
while not top_list.empty():
    i = top_list.get()
    state.top[i] = True
goals = [('achieve_goal', agent, collection_weight)]
treehop.declare_goals(goals)
policy = treehop.pyhop_t(state, goals, True)
treehop.print_policy(policy, state)
gen_expectations(policy, state)
