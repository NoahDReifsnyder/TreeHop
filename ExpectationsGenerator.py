# Takes in a graph from pyhop, performs necessary calculations to add expectations.
import copy
from queue import *
from pyhop import Action
import time
seen = set()
created = set()


class Reg(object):
    def __init__(self):
        self.exp = {}


class Expectations(object):
    def __init__(self):
        self.informed = {}
        self.immediate = {}
        self.regression = {}
        self.goldilocks = {}

    def print(self):
        for exp in vars(self):
            print(exp, getattr(self, exp))


def o_plus(dict_a, dict_b):  # TODO: update other operators to reflect better variable names
    new_dict = {}
    key_list = [x for x in dict_b] + [x for x in dict_a]
    key_list = set(key_list)
    for x in key_list:
        new_dict[x] = {}
        if x in dict_b and x in dict_a:
            new_keys = [y for y in dict_b[x] if y not in dict_a[x]]  # and y not in used_keys]
            for new_key in new_keys:
                new_dict[x][new_key] = dict_b[x][new_key]
            for new_key in dict_a[x]:
                new_dict[x][new_key] = dict_a[x][new_key]
        elif x in dict_b:
            for key in dict_b[x]:
                new_dict[x][key] = dict_b[x][key]
        elif x in dict_a:
            for key in dict_a[x]:
                new_dict[x][key] = dict_a[x][key]
    return new_dict


def o_minus(dict_a, dict_b):
    new_dict = {}
    keys = [x for x in dict_a if x not in dict_b]
    for x in keys:
        new_dict[x] = dict_a[x]
    keys = [x for x in dict_a if x in dict_b]
    for x in keys:
        new_dict[x] = {}
        keys_2 = [y for y in dict_a[x] if y not in dict_b[x]]
        for y in keys_2:
            new_dict[x][y] = dict_a[x][y]
    return new_dict


def o_divide(dict_a, k):
    new_dict = {}
    for key in dict_a:
        new_dict[key] = {}
        for val in dict_a[key]:
            new_dict[key][val] = {}
            for c in dict_a[key][val]:
                new_dict[key][val][c] = dict_a[key][val][c] / k
    return new_dict


def o_times(dict_a, dict_b):
    new_dict = {}
    all_keys = [x for x in dict_b] + [x for x in dict_a]
    all_keys = set(all_keys)
    for x in all_keys:
        new_dict[x] = {}
        if x in dict_b and x in dict_a:
            b_keys = [y for y in dict_b[x] if y not in dict_a[x]]
            a_keys = [y for y in dict_a[x] if y not in dict_b[x]]
            comb_keys = [y for y in dict_a[x] if y in dict_b[x]]
            for key in b_keys:
                new_dict[x][key] = dict_b[x][key]
            for key in a_keys:
                new_dict[x][key] = dict_a[x][key]
            for key in comb_keys:
                new_dict[x][key] = {}
                a_val = [y for y in dict_a[x][key] if y not in dict_b[x][key]]
                b_val = [y for y in dict_b[x][key] if y not in dict_a[x][key]]
                comb_val = [y for y in dict_a[x][key] if y in dict_b[x][key]]
                for val in a_val:
                    new_dict[x][key][val] = dict_a[x][key][val]
                for val in b_val:
                    new_dict[x][key][val] = dict_b[x][key][val]
                for val in comb_val:
                    new_dict[x][key][val] = dict_a[x][key][val] + dict_b[x][key][val]
        elif x in dict_b:
            for key in dict_b[x]:
                new_dict[x][key] = dict_b[x][key]
        elif x in dict_a:
            for key in dict_a[x]:
                new_dict[x][key] = dict_a[x][key]
    return new_dict


class Graph(object):
    def __init__(self, starting_state, policy):
        self.starting_state = starting_state
        self.terminal_nodes = set()
        self.edges = set()
        self.back_edges = set()
        self.cross_edges = set()
        self.vertices = set()
        self.policy = policy
        self.build()

    def build(self):
        queue = Queue()
        queue.put(self.starting_state)
        self.vertices.add(self.starting_state)
        while not queue.empty():
            vertex = queue.get()
            if vertex not in self.policy:  # terminal
                self.terminal_nodes.add(vertex)
                continue
            action = self.policy[vertex]
            self.edges.add((vertex, action))
            self.vertices.add(action)
            for child in action.children:
                self.edges.add((action, child))
                if self.is_parent(child, action):
                    self.back_edges.add((action, child))
                elif child in self.vertices:
                    self.cross_edges.add((action, child))
                if child not in self.vertices:
                    queue.put(child)
                    self.vertices.add(child)
        # count=0
        # for edge in self.edges - self.back_edges:
        #     count+=1
        #     print(len(self.edges-self.back_edges),count)
        #     if (self.is_parent(edge[1],edge[0])):
        #         print("Fuck")
        #         time.sleep(1)1

    def is_parent(self, st, dt):  # determine if st is parent of dt in self, deciding if edge is a back edge
        visited = {}
        for v in self.vertices:
            visited[v] = False
        queue = Queue()
        queue.put(st)
        visited[st] = True
        while not queue.empty():
            new = queue.get()
            if new == dt:
                return True
            children = [x for (y, x) in self.edges-self.back_edges if y == new]
            for child in children:
                if not visited[child]:
                    queue.put(child)
                    visited[child] = True
        return False

    def print(self):
        for var in vars(self):
            if var == "starting_state":
                print(var, getattr(self, var))
            else:
                print(var, len(getattr(self, var)))

    def initialize_expectations(self):
        for v in self.vertices:
            v.expectations = Expectations()

    def gen_immediate(self):
        queue = Queue()
        forward_only = self.edges-self.back_edges-self.cross_edges
        queue.put((self.starting_state, self.starting_state))
        action_type = Action()
        while not queue.empty():
            vertex, parent = queue.get()
            if type(vertex) == type(action_type):  # action, take from parent
                vertex.expectations.immediate = copy.deepcopy(parent.expectations.immediate)
            elif vertex == self.starting_state:  # starting state, no prev effects
                vertex.expectations.immediate = self.policy[vertex].preconditions
            else:  # terminal state
                vertex.expectations.immediate = o_plus({}, parent.effects[vertex])  # replace {} with goals
                pass
            children = [x for (y, x) in forward_only if y == vertex]
            for child in children:
                queue.put((child, vertex))

    def gen_informed(self):
        forward_only = (self.edges - self.back_edges - self.cross_edges)
        queue = Queue()
        queue.put((self.starting_state, self.starting_state))
        action_type = Action()
        while not queue.empty():
            vertex, parent = queue.get()
            parent_expectations = parent.expectations.informed
            if type(vertex) == type(action_type):  # vertex=an Action
                vertex.expectations.informed = copy.deepcopy(parent_expectations)
                pass  # don't change parent_expectations, pass on to grandchildren of preceding state
            elif vertex == self.starting_state:
                pass  # starting state, null informed
            else:  # vertex != s_0 and is a state
                vertex.expectations.informed = o_plus(parent.effects[vertex], copy.deepcopy(parent_expectations))
                pass
            children = [x for (y, x) in forward_only if y == vertex]
            for child in children:
                queue.put((child, vertex))


def comp_num_eff(vertex, num_eff, regression):
    for key in num_eff:
        if key not in regression:
            regression[key] = {}
        for val in num_eff[key]:
            if val in regression[key]:
                keys = [c for c in regression[key][val]]
                for c in keys:
                    prob = regression[key][val][c]
                    eff = num_eff[key][val]
                    temp_min = '-inf'
                    temp_max = 'inf'
                    if isinstance(c[0], (int, float)):  # TODO: Type checking for actions in this format
                        if isinstance(eff[0], (int, float)):
                            temp_min = c[0] - eff[0]
                        else:
                            temp_min = '-inf'
                    if isinstance(c[1], (int, float)):
                        if isinstance(eff[1], (int, float)):
                            temp_max = c[1] - eff[1]
                        else:
                            temp_max = 'inf'
                    regression[key][val].pop(c, None)
                    regression[key][val][(temp_min, temp_max)] = prob
            elif key in vertex.preconditions and val in vertex.preconditions[key]:
                if key not in regression:
                    regression[key] = {}
                if val not in regression[key]:
                    regression[key][val] = {}
                for c in vertex.preconditions[key][val]:
                    regression[key][val][c] = 1
    return regression


class Tau:
    def gen_regressed_expectations(self, exp_type):
        if exp_type == "goldilocks":
            for vertex in self.terminal:
                for key in vertex.node.expectations.informed:
                    if key not in vertex.expectations.goldilocks:
                        vertex.expectations.goldilocks[key] = {}
                    for val in vertex.node.expectations.informed[key]:
                        if val not in vertex.expectations.goldilocks[key]:
                            vertex.expectations.goldilocks[key][val] = {}
                        if not isinstance(vertex.node.expectations.informed[key][val], tuple):
                            vertex.expectations.goldilocks[key][val] = {vertex.node.expectations.informed[key][val]: 1}
        q = Queue()
        action_type = type(Action())
        for vertex in self.terminal:
            q.put((vertex, {}, None))
        while not q.empty():
            vertex, expectations, last_vertex = q.get()
            if type(vertex.node) == action_type:
                num_eff = {}
                for key in vertex.node.effects[last_vertex.node]:
                    for val in vertex.node.effects[last_vertex.node][key]:
                        c = vertex.node.effects[last_vertex.node][key][val]
                        if isinstance(c, tuple):
                            if key not in num_eff:
                                num_eff[key] = {}
                            prev_node = getattr(self.previous_vertex[vertex].node, key)[val]
                            next_node = getattr(last_vertex.node, key)[val]
                            temp_min = next_node[0] - prev_node[0]
                            temp_max = next_node[1] - prev_node[1]
                            num_eff[key][val] = (temp_min, temp_max)
                new_1 = comp_num_eff(vertex, num_eff, expectations)
                new_2 = o_minus((o_minus(vertex.preconditions, vertex.node.effects[last_vertex.node])), expectations)
                new = o_times(new_1, new_2)
                setattr(vertex.expectations, exp_type, o_times(getattr(vertex.expectations, exp_type), new))
                vertex.added += 1
            elif vertex not in self.terminal:
                setattr(vertex.expectations, exp_type, expectations)
                vertex.added += 1
            if vertex.finished():
                if vertex.children > 0:
                    div_result = o_divide(getattr(vertex.expectations, exp_type), vertex.children)
                    setattr(vertex.expectations, exp_type, div_result)
                parents = [x for (x, y) in self.edges if y == vertex]
                for parent in parents:
                    q.put((parent, copy.deepcopy(getattr(vertex.expectations, exp_type)), vertex))
        for node in self.vs:
            if exp_type == "goldilocks":
                vertex = self.vs[node][0]
                vertex.expectations.informed = copy.deepcopy(vertex.node.expectations.informed)
                keys = set([x for x in vertex.expectations.informed] + [x for x in vertex.expectations.regression])
                informed = vertex.expectations.informed
                regression = vertex.expectations.regression
                goldilocks = vertex.expectations.goldilocks
                for key in keys:  # TODO: maybe a better way to do this? it works and it flows quick so maybe leave
                    if key not in node.expectations.goldilocks:
                        node.expectations.goldilocks[key] = {}
                    if key in regression:
                        if key in informed:
                            # key in both
                            vals = set([x for x in informed[key]] + [x for x in regression[key]])
                            for val in vals:
                                if val in regression[key]:
                                    if val in informed[key]:
                                        # val in both
                                        if isinstance(informed[key][val], tuple):
                                            goldilocks[key][val] = (informed[key][val], regression[key][val])
                                    else:
                                        if isinstance(vertex.expectations.regression[key][val], tuple):
                                            goldilocks[key][val] = (None, regression[key][val])
                                        # val only in regression
                                elif val in informed:
                                    # val only in informed
                                    if isinstance(informed[key][val], tuple):
                                        goldilocks[key][val] = (informed[key][val], None)
                        else:
                            # key in only regression
                            for val in regression[key]:
                                if isinstance(regression[key][val], tuple):
                                    goldilocks[key][val] = (None, regression[key][val])
                    elif key in informed:
                        # key in only informed
                        for val in informed[key]:
                            if isinstance(informed[key][val], tuple):
                                goldilocks[key][val] = (informed[key][val], None)
            setattr(node.expectations, exp_type, copy.deepcopy(getattr(self.vs[node][0].expectations, exp_type)))
            for num in self.vs[node]:
                self.vs[node][num].added = 0

    def gen_self(self):
        q = Queue()
        vertex = self.put_vertex(self.starting_state)
        q.put((vertex, set()))
        while not q.empty():
            last_vertex, expanded_be = q.get()
            node = last_vertex.node
            if node in self.graph.terminal_nodes:
                self.terminal.add(last_vertex)
            for edge in self.graph.edges-expanded_be:
                if edge[0] == node:
                    new_expanded_be = set()
                    for e in expanded_be:
                        new_expanded_be.add(e)
                    if edge in self.graph.back_edges:
                        new_expanded_be.add(edge)
                    vertex = self.put_vertex(edge[1])
                    self.edges.add((last_vertex, vertex))
                    q.put((vertex, new_expanded_be))
        action_type = type(Action())
        for node in self.vs:
            for num in self.vs[node]:
                vertex = self.vs[node][num]
                seen.add(vertex)
                vertex.effects = {}
                if type(vertex.node) == action_type:
                    vertex.preconditions = {}
                    for key in vertex.node.preconditions:
                        vertex.preconditions[key] = {}
                        for c in vertex.node.preconditions[key]:
                            vertex.preconditions[key][c] = {}
                            vertex.preconditions[key][c][vertex.node.preconditions[key][c]] = 1
                    for eff_node in vertex.node.effects:
                        vertex.effects[eff_node] = {}
                        for key in vertex.node.effects[eff_node]:
                            vertex.effects[eff_node][key] = {}
                            for c in vertex.node.effects[eff_node][key]:
                                vertex.effects[eff_node][key][c] = {}
                                vertex.effects[eff_node][key][c][vertex.node.effects[eff_node][key][c]] = 1
                vertex.children = len([y for (x, y) in self.edges if x == vertex])
                vertex.set = True
        return

    def get_vertex(self, node, num):
        if node not in self.vs:
            self.vs[node] = {}
        if num not in self.vs[node]:
            self.vs[node][num] = Vertex(node, num)
        return self.vs[node][num]

    def put_vertex(self, node):
        if node not in self.vs:
            self.vs[node] = {}
        num = len(self.vs[node].keys())
        self.vs[node][num] = Vertex(node, num)
        created.add(self.vs[node][num])
        return self.vs[node][num]

    def __init__(self, graph):
        self.graph = graph
        self.starting_state = graph.starting_state
        self.terminal = set()
        self.vs = {}
        self.edges = set()
        self.gen_self()
        self.previous_vertex = {}
        for node in self.vs:
            for num in self.vs[node]:
                vertex = self.vs[node][num]
                parents = [x for (x, y) in self.edges if y == vertex]
                if len(parents) > 1:
                    print("too many parent nodes")
                    time.sleep(10)
                elif len(parents) == 1:
                    self.previous_vertex[vertex] = parents[0]
                else:
                    self.previous_vertex[vertex] = None
        return


class Vertex:
    def __init__(self, node, num):
        self.node = node
        self.num = num
        self.children = 0
        self.added = 0
        self.type = type(node)
        self.set = False
        self.expectations = Expectations()

    def __str__(self):
        return str(self.node) + "," + str(self.num)

    def finished(self):
        if self.children == self.added:
            return True
        else:
            return False


def print_exp(policy):
    for state in policy:
        state.expectations.print()
        print()


def gen_expectations(policy, starting_state):
    graph = Graph(starting_state, policy)
    print("finished graph")
    graph.print()
    graph.initialize_expectations()
    graph.gen_immediate()
    print("finished immediate")
    graph.gen_informed()
    print("finished informed")
    tau = Tau(graph)
    tau.gen_regressed_expectations('regression')
    print("finished regression")
    tau.gen_regressed_expectations('goldilocks')
    print("finished goldilocks")
    # print_exp(policy)
    return
