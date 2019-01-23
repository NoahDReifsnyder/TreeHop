import testing_help as helpper
import copy
helpper.set_domain('BW')
state = copy.deepcopy(helpper.P.state)
while state in helpper.P.policy:
    state = helpper.take_action(state)
print(state.acquired)