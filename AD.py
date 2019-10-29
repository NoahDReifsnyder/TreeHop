import pyhop as treehop
import copy


def prec(state, pre):
    for d in pre:
        for key in pre[d]:
            if not state[d][key] == pre[d][key]:
                return False
    return True


def stack(state, a, b):
    preconditions = {'clear': {a: True, b: True}}
    if prec(state, preconditions):
        state1 = copy.deepcopy(state)
        state2 = copy.deepcopy(state)
        for key in state1:
            if a in state1[key]:
                del(state1[key][a])
        state1['floor'][a] = True
        if a in state2['on']:
            state2['clear'][state['on'][a]] = True
            del(state2['on'][a])
        state2['clear'][b] = False
        state2['on'][a] = b
        state2['clear'][b] = False
        retval = [(state1, .1), (state2, .9)]
        return [state1, state2], preconditions
        pass
    else:
        return False


def unstack(state, a, b):
    preconditions = {'clear': {a: True}, 'on': {a: b}}
    if prec(state, preconditions):
        state1 = copy.deepcopy(state)
        state2 = copy.deepcopy(state)
        for key in state1:
            if a in state1[key]:
                del(state1[key][a])
        state1['floor'][a] = True
        del(state2['on'][a])
        state2['clear'][b] = True
        return state1
    else:
        return False
    pass


