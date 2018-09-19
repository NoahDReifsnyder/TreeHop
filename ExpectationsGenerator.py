#Takes in a graph from pyhop, performs necessary calculations to add expectations.
import copy
def genExpectations(tree):
    edges=tree.edges
    verticies=tree.verticies
    tree=tree.children[0]
    print(tree)
    print(edges)
    print(verticies)
    print(len(edges),len(verticies))
    test=set()
    for v in verticies:
        test.add(v._num)
    print(len(test))
    return
edges=[]
verticies=[]
def dfs(tree):
    print(tree.name,len(tree.children))
    for child in tree.children:
        dfs(child)