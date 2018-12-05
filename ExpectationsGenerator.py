#Takes in a graph from pyhop, performs necessary calculations to add expectations.
import copy
from queue import *
from pyhop import Action
import time

class Reg(object):
    def __init__(self):
        self.exp={} 

class Expectations(object):
    def __init__(self):
        self.informed = {}
        self.immediate = {}
        self.regression = {}
        self.goldilocks = {}
    def print(self):
        for exp in vars(self):
            print(exp, getattr(self, exp))


def o_plus(left,right):
    new_dict={}
    l=[x for x in right if x not in left]
    for x in l:
        new_dict[x]=right[x]
    for x in left:
        new_dict[x]=left[x]
    # print(left)
    # print(right)
    # print(new_dict)
    return new_dict
def o_minus(left,right):
    new_dict={}
    l=[x for x in left if x not in right]
    for x in l:
        new_dict[x]=left[x]
    return new_dict
def o_divide(left,right):
    return
def o_times(left,right):
    return

class Graph(object):
    def __init__(self,starting_state,policy):
        self.starting_state = starting_state
        self.terminal_nodes = set()
        self.edges = set()
        self.back_edges = set()
        self.cross_edges = set()
        self.vertices = set()
        self.policy = policy
        self.rev_policy={}
        for state in policy:
            self.rev_policy[policy[state]]=state
        self.inverse_policy = {v: k for k, v in policy.items()}
        self.build()
        self.add_back_edges()

    def add_back_edges(self):
        return

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

    def is_parent(self, st, dt):  # determine if st is parent of dt in self, for deciding if edge is a backedge in buildself
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
            children = [x for (y, x) in self.edges-self.back_edges if y == new ]
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
        for v in self.policy:
            v.expectations.immediate=o_plus(self.policy[v].precond,self.rev_policy[v].effects)
            self.policy[v].expectations.immediate=v.expectations.immediate

    def gen_informed(self):
        forward_only = (self.edges - self.back_edges - self.cross_edges)
        queue = Queue()
        queue.put((self.starting_state, {}))
        action_type = Action()
        while not queue.empty():
            vertex, parent_expectations = queue.get()
            if vertex == self.starting_state:  # vertex=s_0
                pass  # expectations are null
            elif type(vertex) == type(action_type):  # vertex=an Action
                vertex.expectations.informed = copy.deepcopy(parent_expectations)
                pass  # don't change parent_expectations, pass on to grandchildren of preceding state
            else:  # vertex != s_0 and is a state
                vertex.expectations.informed = copy.deepcopy(parent_expectations)
                pass
            children = [x for (y, x) in forward_only if y == vertex]
            # print(vertex.expectations.informed)
            for child in children:
                compound_expectations=copy.deepcopy(parent_expectations)
                if type(vertex) == type(action_type):
                    for attr in vertex.effects[child]:  # compound function
                        if attr not in compound_expectations:
                            compound_expectations[attr] = {}
                        for v in vertex.effects[child][attr]:
                            compound_expectations[attr][v] = vertex.effects[child][attr][v]
                queue.put((child, compound_expectations))

    def gen_regression(self):
        print(self.edges)
        print(self.terminal_nodes)
        expanded=Queue()
        for node in self.terminal_nodes:
            expanded.put(node)
        expanded_edges=set()
        count=0
        while not expanded.empty():
            node=expanded.get()
            for edge in self.edges-expanded_edges:
                if edge[1]==node:
                    if edge in self.back_edges or edge in self.cross_edges:
                        expanded_edges.add(edge)
                    expanded.put(edge[0])
        return

    def gen_goldilocks(self):
        return


class Vertex:
    vs={}
    def __init__(self,node,num):
        self.node=node
        self.num=num
        self.type=type(node)
    def __str__(self):
        return str(self.node)+","+str(self.num)
def get_vertex(node,num):
    if node not in Vertex.vs:
        Vertex.vs[node]={}
    if num not in Vertex.vs[node]:
        Vertex.vs[node][num]=Vertex(node,num)
    return Vertex.vs[node][num]

def gen_expectations(policy, starting_state):
    print('here')
    graph = Graph(starting_state, policy)
    print("finished graph")
    graph.print()
    graph.initialize_expectations()
    graph.gen_immediate()
    print("finished immediate")
    # graph.gen_informed()
    # print("finished informed")
    # graph.gen_regression()
    # print("finished regression")
    # graph.gen_goldilocks()
    # print("finished goldilocks")
    for state in policy:
        state.expectations.print()
    # for state in graph.terminal_nodes:
    #     print(state.lit)
    #     state.expectations.print()
    return




