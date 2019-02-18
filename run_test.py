import testing_help as helpper
import copy
import random
from queue import Queue
import time
num_examples = 100
mw_modifier = 0
mw_modified = False

def mw_disc(state):
    global mw_modifier, mw_modified
    if not state.repair['Agent1']:
        mw_modified = False
        mw_modifier = 0
    decider = random.randint(0,100)
    if decider < 6:
        mw_modified = True
        mw_modifier = 3
        state.repair['Agent'] = True
    if 20 < decider < 26:
        prev = state.fuel['Beacon']
        if prev[0] >= 1:
            state.fuel['Beacon'] = (prev[0] - 1, prev[1] - 1)



def run_mw():
    fuel_consumed = {'title': 'Fuel Consumed'}
    refuels = 0
    for expectation in helpper.expectation_types:
        fuel_consumed[expectation] = {}
        for i in range(0, num_examples):
            fuel_consumed[expectation][i] = 0
            print(i)
            helpper.set_domain('MW')
            state = copy.deepcopy(helpper.P.state)
            print('start', state.lit)
            prev_fuel = state.fuel['Agent1'][0]
            actions = Queue()
            while state in helpper.P.policy:
                action = helpper.P.policy[state]
                actions.put(action)
                state = action.children[0]
            state = copy.deepcopy(helpper.P.state)
            while not actions.empty():
                action = actions.get()
                action_name = action.name
                action_expectations = action.expectations
                if not helpper.check_expectations(state, action_expectations, expectation):
                    print("oof")
                    helpper.replan(state)
                    actions = Queue()
                    while state in helpper.P.policy:
                        action = helpper.P.policy[state]
                        actions.put(action)
                        state = action.children[0]
                    continue
                # if action.name[0] == 'light':
                #     print('here1', state.fuel)
                state = helpper.take_action(state, action, i, expectation)
                if not state:
                    break
                mw_disc(state)
                #print(action.name, state.fuel)
                fixed_fuel = state.fuel['Agent1'][0] + mw_modifier
                state.fuel['Agent1'] = (fixed_fuel, fixed_fuel)
                new_fuel = state.fuel['Agent1'][0]
                delta_fuel = prev_fuel - new_fuel
                if action_name[0] != 'refuel':
                    fuel_consumed[expectation][i] += delta_fuel
                else:
                    refuels += 1
                prev_fuel = new_fuel
            if state:
                print(state.lit, state.fuel)
            else:
                print('Failed')
    helpper.plot([fuel_consumed])


def bw_disc(state):
    # disc is that blocks dissapear from quarry, or from my stack.
    # print(state.on, state.under, state.top, state.top_acquired)
    decider = random.randint(0, 100)
    keys = None
    if decider < 10 or decider > 90:
        keys = [key for key in vars(state) if '_' not in key and not (key == 'expectations' or key == 'acquired')]
    if decider < 10:
        # quarry
        blocks = [x for x in state.collected if not state.collected[x]]
        if blocks:
            block = random.choice(blocks)
            remove_block(state, block)
            for key in keys:
                temp = getattr(state, key)
                del temp[block]
    elif decider > 90:
        # self
        blocks = [x for x in state.collected if state.collected[x]]
        if blocks:
            block = random.choice(blocks)
            remove_block(state, block)
            for key in keys:
                temp = getattr(state, key)
                del temp[block]


def remove_block(state, block):
    on = state.on[block]
    under = state.under[block]
    state.on[under] = on
    state.under[on] = under
    if state.collected[block]:
        mass = state.weights[block]
        mass = round((mass[0] + mass[1]) / 2, 0)
        old_mass = state.acquired['Agent1']
        state.acquired['Agent1'] = (old_mass[0] - mass, old_mass[1] - mass)


def run_bw():
    mass_obtained = {'title': "Mass Obtained"}
    for expectation in helpper.expectation_types:
        mass_obtained[expectation]={}
        for i in range(0, num_examples):
            print(i)
            mass_obtained[expectation][i] = 0
            helpper.set_domain('BW')
            state = copy.deepcopy(helpper.P.state)
            prev_mass = state.acquired['Agent1'][0]
            actions = Queue()
            while state in helpper.P.policy:
                action = helpper.P.policy[state]
                actions.put(action)
                state = action.children[0]
            state = copy.deepcopy(helpper.P.state)
            while not actions.empty():
                action = actions.get()
                action_name = action.name
                expectations = action.expectations
                if not helpper.check_expectations(state, expectations, expectation):
                    print("oof")
                    helpper.replan(state)
                    actions = Queue()
                    while state in helpper.P.policy:
                        action = helpper.P.policy[state]
                        actions.put(action)
                        state = action.children[0]
                    continue
                state = helpper.take_action(state, action, i, expectation)
                if not state:
                    break
                new_mass = state.acquired['Agent1'][0]
                bw_disc(state)
                delta_mass = new_mass - prev_mass
                mass_obtained[expectation][i] += delta_mass
                prev_mass = state.acquired['Agent1'][0]
            if state:
                print(state.acquired)
                if state.acquired['Agent1'][0]<500:
                    print("\n\n\n\n")
                    helpper.add_error(expectation)
            else:
                print('Failed')
            pass
        pass
    helpper.plot([mass_obtained])


run_bw()
