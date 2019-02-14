import testing_help as helpper
import copy
import random
import time
num_examples = 25
mw_modifier = 0
mw_modified = False

def mw_disc(state):
    global mw_modifier, mw_modified
    if not state.repair['Agent1']:
        mw_modified = False
        mw_modifier = 0
    decider = random.randint(0,100)
    if decider < 10:
        mw_modified = True
        mw_modifier = 3
        state.repair['Agent'] = True


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
            prev_fuel = state.fuel['Agent1'][0]
            while state in helpper.P.policy:
                action_name = helpper.P.policy[state].name
                action_expectations = helpper.P.policy[state].expectations
                action = helpper.P.policy[state]
                if not helpper.check_expectations(state, action_expectations, expectation):
                    print("oof")
                    helpper.replan(state)
                    continue
                state = helpper.take_action(state, action, i, expectation)
                mw_disc(state)
                fixed_fuel = state.fuel['Agent1'][0] + mw_modifier
                state.fuel['Agent1'] = (fixed_fuel, fixed_fuel)
                new_fuel = state.fuel['Agent1'][0]
                delta_fuel = prev_fuel - new_fuel
                if action_name[0] != 'refuel':
                    fuel_consumed[expectation][i] += delta_fuel
                else:
                    refuels += 1
                prev_fuel = new_fuel
            print(state.lit)
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
            while state in helpper.P.policy:
                action_name = helpper.P.policy[state].name
                action = helpper.P.policy[state]
                if not helpper.check_expectations(state, state.expectations, expectation):
                    print(action_name)
                    print("oof")
                state = helpper.take_action(state, action, i, expectation)
                bw_disc(state)
                new_mass = state.acquired['Agent1'][0]
                delta_mass = new_mass - prev_mass
                mass_obtained[expectation][i] += delta_mass
                prev_mass = new_mass
            pass
        pass
    helpper.plot([mass_obtained])


run_bw()
