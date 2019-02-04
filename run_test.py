import testing_help as helpper
import copy
import matplotlib.pyplot as plt


num_examples = 100


def run_mw():
    fuel_consumed = 0
    actions_taken = 0
    refuels = 0
    action_graph = {}
    fuel_graph = {}
    for i in range(0, num_examples):
        print(i)
        helpper.set_domain('MW')
        state = copy.deepcopy(helpper.P.state)
        prev_fuel = state.fuel['Agent1'][0]
        while state in helpper.P.policy:
            action_name = helpper.P.policy[state].name
            action_expectations = helpper.P.policy[state].expectations
            if not helpper.check_expectations(state, action_expectations, "immediate"):
                print(action_name)
                print("oof")
            state = helpper.take_action(state)
            actions_taken += 1
            new_fuel = state.fuel['Agent1'][0]
            delta_fuel = prev_fuel - new_fuel
            if action_name[0] != 'refuel':
                fuel_consumed += delta_fuel
            else:
                refuels += 1
            prev_fuel = new_fuel
        action_graph[i] = actions_taken
        fuel_graph[i] = fuel_consumed
    action_lists = sorted(action_graph.items())
    fuel_lists = sorted(fuel_graph.items())
    action_x, action_y = zip(*action_lists)
    fuel_x, fuel_y = zip(*fuel_lists)
    plt.plot(fuel_x, fuel_y)
    plt.plot(action_x, action_y)
    plt.show()


def run_bw():
    mass_obtained = 0
    action_taken = 0
    for i in range(0, num_examples):
        print(i)
        helpper.set_domain('BW')
        state = copy.deepcopy(helpper.P.state)
        prev_mass = state.acquired['Agent1'][0]
        while state in helpper.P.policy:
            action_name = helpper.P.policy[state].name
            action_expectations = helpper.P.policy[state].expectations
            if not helpper.check_expectations(state, action_expectations, "immediate"):
                print(action_name)
                print("oof")
            state = helpper.take_action(state)
            action_taken += 1
            new_mass = state.acquired['Agent1'][0]
            delta_mass = new_mass - prev_mass
            mass_obtained += delta_mass
            prev_mass = new_mass
        pass
    pass


run_bw()
