# Grid World Problem File
from MWD import *
from random import *
from ExpectationsGenerator import *
state = None
policy = None

def run():
    global state, policy
    state = treehop.State('state')
    state.above = {}
    state.behind = {}
    state.below = {}
    state.in_front = {}
    state.lit = {"B1": 0, "B2": 0, "B3": 0}
    state.beacons = {}
    state.agent = {'Agent1': None}
    state.fuel = {'Agent1': (10, 10), 'Beacon': (3, 3)}
    treehop.declare_numeric("fuel")
    state.max_fuel = copy.deepcopy(state.fuel)
    state.repair = {'Agent1': False}
    n = 10
    position = n * n - 1
    state.agent['Agent1'] = position
    placed = []
    for b in state.lit:
        x = randint(1, n*n)
        while x in placed:
            x = randint(1, n*n)
        placed.append(x)
        state.beacons[b] = x
    i = 1
    while i <= n**2:
        if i <= n:
            if i == 1:
                state.behind[i] = i+1
            elif i == n:
                state.in_front[i] = i - 1
            else:
                state.behind[i] = i+1
                state.in_front[i] = i - 1
            state.above[i] = i+n
        elif i > (n**2-n):
            if i == (n**2-n+1):
                state.behind[i] = i+1
            elif i == n**2:
                state.in_front[i] = i - 1
            else:
                state.behind[i] = i+1
                state.in_front[i] = i - 1
            state.below[i] = i-n
        elif (i-1) % n == 0:
            state.below[i] = i-n
            state.above[i] = i+n
            state.behind[i] = i+1
        elif i % n == 0:
            state.below[i] = i-n
            state.above[i] = i+n
            state.in_front[i] = i - 1
        else:
            state.below[i] = i-n
            state.above[i] = i+n
            state.in_front[i] = i - 1
            state.behind[i] = i+1
        i = i+1
    treehop.reset()
    goals = [('light_all', 'Agent1', n)]
    treehop.declare_goals(goals)
    policy = treehop.pyhop_t(state, original_call=True)
    # treehop.print_policy(policy, state)
    # treehop.print_state(state)
    gen_expectations(policy, state)

