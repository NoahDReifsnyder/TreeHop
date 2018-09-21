#Takes in a graph from pyhop, performs necessary calculations to add expectations.
import copy
def genExpectations(policy,starting_state):
    graph=buildGraph(policy)
    for member in graph:
        print(member,len(graph[member]))
    return
def buildGraph(policy):
    e="edges"
    be="back_edges"
    ce="cross_edges"
    v="verticies"
    graph={e:set(),be:set(),ce:set(),v:set()}
    for state in policy:
        action=policy[state]
        graph[e].add((state,action))
        for child in action.children:
            graph[e].add((action,child))
        graph[v].add(state)
        graph[v].add(action)
    return graph