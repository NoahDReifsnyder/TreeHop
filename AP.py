from AD import *


def main(n):
    state = treehop.State('state')
    state.clear = {}
    state.floor = {}
    state.on = {}
    for i in range(2*n):
        state.clear[i] = True
    goals = [('achieve_goal', n)]
    use_state = copy.deepcopy(state)
    policy = treehop.pyhop_t(state, goals, True)
    #print(use_state)
    treehop.print_policy(policy, use_state)
    #print(policy)

main(10)