#Takes in a graph from pyhop, performs necessary calculations to add expectations.
import copy
from queue import *
class Expectations(object):
    def __init__(self):
        self.informed={}
        self.immediate={}
        self.regression={}
        self.goldilocks={}
        return
class Graph(object):
    def __init__(self,starting_state):
        self.starting_state=starting_state
        self.edges=set()
        self.back_edges=set()
        self.cross_edges=set()
        self.verticies=set()
    def print(self):
        for var in vars(self):
            if var=="starting_state":
                print(var,getattr(self,var))
            else:
                print(var, len(getattr(self, var)))
    def initialize_expectations(self):
        for v in self.verticies:
            v.expectations=Expectations()
def genExpectations(policy,starting_state):
    graph=buildGraph(policy,starting_state)
    graph.print()
    graph.initialize_expectations()
    return

def genImmediate(graph):
    return

def genInformed(graph):
    forward_only=(graph.edges-graph.back_edges-graph.cross_edges)
    return

def genRegression(graph):
    return

def genGoldilocks(graph):
    return
def buildGraph(policy,starting_state):#adds verticies and edges, and initialized graph components back and cross edges.
    graph=Graph(starting_state)
    queue=Queue()
    queue.put(starting_state)
    graph.verticies.add(starting_state)
    while not queue.empty():
        state=queue.get()
        if state not in policy:#terminal
            #print(state.lit)
            continue
        action=policy[state]
        graph.edges.add((state,action))
        graph.verticies.add(action)
        for child in action.children:
            graph.edges.add((action,child))
            if isParent(graph,child,action):
                graph.back_edges.add((action, child))
            elif child in graph.verticies:
                graph.cross_edges.add((action, child))
            if child not in graph.verticies:
                queue.put(child)
                graph.verticies.add(child)
    return graph

def isParent(graph,st,dt):#determine if st is parent of dt in graph, for deciding if edge is a backedge in buildGraph
    visited={}
    for v in graph.verticies:
        visited[v]=False
    queue=Queue()
    queue.put(st)
    visited[st]=True
    while not queue.empty():
        new=queue.get()
        if type(new)==type(dt) and new==dt:
            return True
        children=[x for (y,x) in graph.edges if type(y) == type(new) and y == new]
        for child in children:
            if not visited[child]:
                queue.put(child)
                visited[child]=True
    return False