import AD

state = {'clear': {1: True, 2: False, 3: True}, 'on': {1: 2}, 'floor': {}}

state = AD.stack(state, 1, 3)
print(state)