#Grid World Problem File
from __future__ import print_function
import pyhop as treehop
from testD import *
from collections import defaultdict
from random import *
import collections
from ExpectationsGenerator import *
import time


state=treehop.State('state')
state.on={}
state.clear={}
state.energy={1:[100,100]}
numBlocks=100
towerSize=10
chanceToStack=10
stacked=[]
for i in range(numBlocks):
    state.clear[i]=True
for i in range(numBlocks):
    rand=randint(1,100)
    block=None
    if rand<chanceToStack:
        block=randint(0,numBlocks-1)
        if block==0:
            start=99
        else:
            start=block-1
        while block in stacked or block==i:
            if block==99:
                block=0
            elif block==start:
                block=None
                break
            else:
                block+=1
    if i==block:
        print('here')
        time.sleep(5)
    state.on[i]=block
    if block!=None:
        stacked.append(block)
        state.clear[block]=False

goals=[('achieve_goal', towerSize)]
treehop.declare_goals(goals)
treehop.declare_numeric('energy')
policy=treehop.pyhopT(state, goals,True)
treehop.print_policy(policy,state)
test1={'energy':{1:{2:.5, 3:.5}}}
test2={'energy':{1:{2:.5, 3:.5}}}
print(o_divide(o_times(test1,test2),2))
gen_expectations(policy, state)
#treehop.print_plan_dfs(actions)
#print_plan(Plan,exp='Rexp')

