#Takes in a graph from pyhop, performs necessary calculations to add expectations.
import copy
from queue import *
def genExpectations(policy,starting_state):
    graph=buildGraph(policy,starting_state)
    for member in graph:
        print(member,len(graph[member]))
    return
def buildGraph(policy,starting_state):#adds verticies and edges, and initialized graph components back and cross edges.
    e = "edges"
    be = "back_edges"
    ce = "cross_edges"
    v = "verticies"
    graph={e:set(),be:set(),ce:set(),v:set()}
    queue=Queue()
    queue.put(starting_state)
    visited=[]
    while not queue.empty():
        state=queue.get()
        if state not in policy:
            print(state.lit)
            continue
        action=policy[state]
        graph[e].add((state,action))
        for child in action.children:
            graph[e].add((action,child))
            if child not in visited:
                queue.put(child)
                visited.append(child)
        graph[v].add(state)
        graph[v].add(action)
    return graph
