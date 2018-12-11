#Takes in a graph from pyhop, performs necessary calculations to add expectations.
import copy
from queue import *
from pyhop import Action,numerics
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


def compound(A,B):
    print(A,B)
    return B.replace("X","("+A+")")

def o_plus(A, B):
    new_dict={}
    l=[x for x in B]+[x for x in A]
    print(A)
    print(B)
    l=set(l)
    print(l)
    for x in l:
        new_dict[x]={}
        if x in B and x in A:
            if x in numerics:
                keys=[y for y in B[x] if y in A[x]]
                for key in keys:
                    new_dict[x][key]=compound(A[x][key],B[x][key])
                new_keys = [y for y in A[x] if y not in keys]
                for key in new_keys:
                    new_dict[x][key] = A[x][key]
                new_keys = [y for y in B[x] if y not in keys]
                for key in new_keys:
                    new_dict[x][key] = B[x][key]
            else:
                keys=[y for y in B[x] if y not in A[x]]
                for key in keys:
                    new_dict[x][key] = B[x][key]
                for key in A[x]:
                    new_dict[x][key] = A[x][key]
        elif x in B:
            for key in B[x]:
                new_dict[x][key] = B[x][key]
        elif x in A:
            for key in A[x]:
                new_dict[x][key] = A[x][key]
    print(new_dict)
    print('')

    return new_dict
def o_minus(A, B):
    new_dict={}
    l=[x for x in A if x not in B]
    for x in l:
        new_dict[x]=A[x]
    return new_dict
def o_divide(A, k):
    return
def o_times(A,B):
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
        self.inverse_policy={}
        print(policy[starting_state].effects)
        for state in policy:
            for effect_state in policy[state].effects:
                self.inverse_policy[effect_state]=policy[state]
        for state in self.inverse_policy:
            print(state)
        #self.inverse_policy = {v: k for k, v in policy.items()}
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
            if v == self.starting_state:
                v.expectations.immediate=self.policy[v].precond
            else:
                v.expectations.immediate=o_plus(self.policy[v].precond,self.inverse_policy[v].effects[v])
            self.policy[v].expectations.immediate=v.expectations.immediate

    def gen_informed(self):
        forward_only = (self.edges - self.back_edges - self.cross_edges)
        queue = Queue()
        queue.put((self.starting_state, {}))
        action_type = Action()
        while not queue.empty():
            vertex, parent_expectations = queue.get()
            if type(vertex) == type(action_type):  # vertex=an Action
                vertex.expectations.informed = copy.deepcopy(parent_expectations)
                pass  # don't change parent_expectations, pass on to grandchildren of preceding state
            elif vertex==self.starting_state:
                pass #starting state, null informed
            else:  # vertex != s_0 and is a state
                vertex.expectations.informed = o_plus(self.inverse_policy[vertex].effects[vertex],copy.deepcopy(parent_expectations))
                pass
            children = [x for (y, x) in forward_only if y == vertex]
            # print(vertex.expectations.informed)
            for child in children:
                compound_expectations=copy.deepcopy(vertex.expectations.informed)
                # if type(vertex) == type(action_type):
                #     for attr in vertex.effects[child]:  # compound function
                #         if attr not in compound_expectations:
                #             compound_expectations[attr] = {}
                #         for v in vertex.effects[child][attr]:
                #             compound_expectations[attr][v] = vertex.effects[child][attr][v]
                queue.put((child, compound_expectations))

    def gen_regression(self):
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
    print('here',numerics)
    graph = Graph(starting_state, policy)
    print("finished graph")
    graph.print()
    graph.initialize_expectations()
    graph.gen_immediate()
    print("finished immediate")
    graph.gen_informed()
    print("finished informed")
    # graph.gen_regression()
    # print("finished regression")
    # graph.gen_goldilocks()
    # print("finished goldilocks")
    for state in policy:
        state.expectations.print()
    test()
    # for state in graph.terminal_nodes:
    #     print(state.lit)
    #     state.expectations.print()
    return




