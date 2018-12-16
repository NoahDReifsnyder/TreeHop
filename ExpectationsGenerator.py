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


def o_plus(A, B):
    new_dict={}
    l=[x for x in B]+[x for x in A]
    l=set(l)
    for x in l:
        new_dict[x]={}
        if x in B and x in A:
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
    return new_dict

def o_minus(A, B):
    new_dict={}
    l=[x for x in A if x not in B]
    for x in l:
        new_dict[x]=A[x]
    return new_dict

def o_divide(A, k):
    new_dict={}
    for key in A:
        new_dict[key]={}
        for val in A[key]:
            new_dict[key][val]={}
            for c in A[key][val]:
                new_dict[key][val][c]=A[key][val][c]/k
    return new_dict

def o_times(A,B):
    new_dict = {}
    l = [x for x in B] + [x for x in A]
    l = set(l)
    for x in l:
        new_dict[x] = {}
        if x in B and x in A:
            BKeys = [y for y in B[x] if y not in A[x]]
            AKeys = [y for y in A[x] if y not in B[x]]
            CombKeys = [y for y in A[x] if y in B[x]]
            for key in BKeys:
                new_dict[x][key] = B[x][key]
            for key in AKeys:
                new_dict[x][key] = A[x][key]
            for key in CombKeys:
                new_dict[x][key]={}
                AVals=[y for y in A[x][key] if y not in B[x][key]]
                BVals=[y for y in B[x][key] if y not in A[x][key]]
                CombVals=[y for y in A[x][key] if y in B[x][key]]
                for val in AVals:
                    new_dict[x][key][val]=A[x][key][val]
                for val in BVals:
                    new_dict[x][key][val]=B[x][key][val]
                for val in CombVals:
                    new_dict[x][key][val]=A[x][key][val]+B[x][key][val]
        elif x in B:
            for key in B[x]:
                new_dict[x][key] = B[x][key]
        elif x in A:
            for key in A[x]:
                new_dict[x][key] = A[x][key]
    return new_dict

class Graph(object):
    def __init__(self,starting_state,policy):
        self.starting_state = starting_state
        self.terminal_nodes = set()
        self.edges = set()
        self.back_edges = set()
        self.cross_edges = set()
        self.vertices = set()
        self.policy = policy
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
        queue=Queue()
        forward_only=self.edges-self.back_edges-self.cross_edges
        queue.put((self.starting_state,self.starting_state))
        action_type = Action()
        while not queue.empty():
            vertex, parent=queue.get()
            if type(vertex)==type(action_type): #action, take from parent
                vertex.expectations.immediate=copy.deepcopy(parent.expectations.immediate)
            elif vertex == self.starting_state: #starting state, no prev effects
                vertex.expectations.immediate=self.policy[vertex].precond
            else: #terminal state
                vertex.expectations.immediate=o_plus({},parent.effects[vertex]) #replace {} with goals if ever needed
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
            parent_expectations=parent.expectations.informed
            if type(vertex) == type(action_type):  # vertex=an Action
                vertex.expectations.informed = copy.deepcopy(parent_expectations)
                pass  # don't change parent_expectations, pass on to grandchildren of preceding state
            elif vertex==self.starting_state:
                pass #starting state, null informed
            else:  # vertex != s_0 and is a state
                vertex.expectations.informed = o_plus(parent.effects[vertex],copy.deepcopy(parent_expectations))
                pass
            children = [x for (y, x) in forward_only if y == vertex]
            for child in children:
                queue.put((child, vertex))

class Tau:
    def gen_regression(self):
        q=Queue()
        action_type=type(Action())
        for vertex in self.terminal:
            q.put(vertex)
        while not q.empty():
            vertex=q.get()
            if type(vertex.node) == action_type:
                vertex.precond={}
                for key in vertex.node.precond:
                    vertex.precond[key] = {}
                    for c in vertex.node.precond[key]:
                        vertex.precond[key][c] = 1
            if vertex in self.terminal:
                pass
            if vertex.finished():
                parents=[x for (x,y) in self.edges if y == vertex]
                for parent in parents:
                    print(parent)
                    q.put(parent)

    def gen_self(self):
        graph=self.graph
        q=Queue()
        vertex=self.put_vertex(self.starting_state)
        q.put((vertex,set()))
        test=set()
        print(len(graph.back_edges))
        while not q.empty():
            last_vertex,expanded_be=q.get()
            print(last_vertex,expanded_be)
            node=last_vertex.node
            print(node)
            if node in self.graph.terminal_nodes:
                self.terminal.add(last_vertex)
            print(self.terminal)
            for edge in expanded_be:
                if edge not in self.graph.back_edges:
                    print(edge)
                    time.sleep(10)
            for edge in self.graph.edges-expanded_be:
                if edge[0]==node:
                    new_expanded_be = copy.deepcopy(expanded_be)
                    print(new_expanded_be == expanded_be)
                    if edge in self.graph.back_edges:
                        new_expanded_be.add(edge)
                        print(edge, edge in self.graph.back_edges)
                    vertex=self.put_vertex(edge[1])
                    q.put((vertex,new_expanded_be))
            # last_vertex,expanded_be=q.get()
            # if len(expanded_be)> len(graph.back_edges):
            #     print("how")
            #     print(expanded_be)
            #     print(graph.back_edges)
            #     for edge in test:
            #         print(edge in expanded_be)
            #         #print(edge in graph.back_edges)
            #     time.sleep(10)
            # node=last_vertex.node
            # if node in self.graph.terminal_nodes:
            #     self.terminal.add(last_vertex)
            # for edge in graph.edges-expanded_be:
            #     if edge[0]==node:
            #         new_expanded_be=copy.deepcopy(expanded_be)
            #         temp=[(x,y) for (x,y) in graph.back_edges if (x,y)==(edge[0],edge[1])]
            #         if edge in graph.back_edges:
            #             for t in temp:
            #                 for e in graph.back_edges:
            #                     if e[1] == t[1] and e[0] == t[0]:
            #                         print(e,t)
            #                         test.add(e)
            #                         new_expanded_be.add(e)
            #                         print(e in new_expanded_be)
            #         vertex = self.put_vertex(edge[1])
            #         self.edges.add((last_vertex,vertex))
            #         q.put((vertex,copy.deepcopy(new_expanded_be)))
            #     pass
        for node in self.vs:
            for num in self.vs[node]:
                vertex=self.vs[node][num]
                vertex.children=len([x for (x,y) in self.edges if x == vertex])
                #print(vertex,vertex.children)
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
        return self.vs[node][num]

    def __init__(self,graph):
        self.graph=graph
        self.starting_state=graph.starting_state
        self.terminal=set()
        self.verticies=set()
        self.vs={}
        self.edges=set()
        self.gen_self()
        return
class Vertex:
    def __init__(self,node,num):
        self.node=node
        self.num=num
        self.children=0
        self.added=0
        self.type=type(node)
        self.expectations=Expectations()
    def __str__(self):
        return str(self.node)+","+str(self.num)
    def finished(self):
        return False

def print_exp(policy):
    for state in policy:
        state.expectations.print()

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
    tau=Tau(graph)
    #tau.gen_regression()
    #print("finished regression")
    # graph.gen_goldilocks()
    # print("finished goldilocks")
    #print_exp(policy)
    return




