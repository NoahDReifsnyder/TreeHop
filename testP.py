#Grid World Problem File
from __future__ import print_function
import pyhop as treehop
from MWD import *
from collections import defaultdict
from random import *
from ExpectationsGenerator import gen_expectations



state=treehop.State('state')
state.above={}
state.behind={}
state.below={}
state.infront={}
state.lit={"B1":0,"B2":0,"B3":0}
state.beacons={}
state.agent={'Agent1':1}
state.clear={}
state.fuel={'Agent1':10}
n=5
placed=[]
for b in state.lit:
    x=randint(1,n*n)
    while x in placed:
        x=randint(1,n*n)
    placed.append(x)
    state.beacons[b]=x
i=1
while i<=n**2:
    state.clear[i]=1
    if i<=n:
        if i==1:
            state.behind[i]=i+1
        elif i==n:
            state.infront[i]=i-1
        else:
            state.behind[i]=i+1
            state.infront[i]=i-1
        state.above[i]=i+n
    elif i>(n**2-n):
        if i==(n**2-n+1):
            state.behind[i]=i+1
        elif i==n**2:
            state.infront[i]=i-1
        else:
            state.behind[i]=i+1
            state.infront[i]=i-1
        state.below[i]=i-n
    elif (i-1)%n==0:
        state.below[i]=i-n
        state.above[i]=i+n
        state.behind[i]=i+1
    elif i%n==0:
        state.below[i]=i-n
        state.above[i]=i+n
        state.infront[i]=i-1
    else:
        state.below[i]=i-n
        state.above[i]=i+n
        state.infront[i]=i-1
        state.behind[i]=i+1
    i=i+1

goals=[('light_all', 'Agent1', n)]
treehop.declare_goals(goals)
policy=treehop.pyhopT(state, goals,True)
#treehop.print_policy(policy,state)

gen_expectations(policy, state)
#treehop.print_plan_dfs(actions)
#print_plan(Plan,exp='Rexp')

