#Takes in a graph from pyhop, performs necessary calculations to add expectations.
import copy
def genExpectations(policy,starting_state):
    print(len(policy))
    print(starting_state in policy)
    print(policy[starting_state].name)
    return
edges=[]
back_edges=[]
cross_edges=[]
verticies=[]
def dfs(tree):
    print(tree.name,len(tree.children))
    for child in tree.children:
        dfs(child)