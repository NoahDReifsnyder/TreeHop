#Takes in a graph from pyhop, performs necessary calculations to add expectations.
def genExpectations(tree):
    edges=tree.edges
    verticies=tree.verticies
    tree=tree.children[0]
    print(tree)
    print(edges)
    print(verticies)
    print(len(edges),len(verticies))
    dfs(tree)
    return
edges=[]
verticies=[]
def dfs(tree):
    print(tree.name,len(tree.children))
    for child in tree.children:
        dfs(child)