#Grid World Domain File With Preconditions Sent To Planner
#Conformant Planning for refuelling
import pyhop as treehop
import copy
from random import *
from collections import defaultdict
#nprecond={dict:{1:(denom:val)}}
Geff=1
err=.1
ND=False #Action type



#forward or up
def stack(state, block1,block2):
    state1=copy.copy(state)
    if state.clear[block1] and state.clear[block2] and state.energy[1]>=10:
        precond={'clear':{block1:True, block2:True},'energy':{1:('>=',10)}}
        state.on[block1] = block2
        state.clear[block2]=False
        state.energy[1]-=10
        numeric_effects={'energy':{1:"X-10"}}
        numeric_effects1={'energy':{1:"X-10"}}
        if ND:
            if not state.clear[state.infront[loc]]:
                return False
            precond['clear'][state.infront[loc]]=1
            return ([state,state1],precond,[numeric_effects,numeric_effects2])
        else:
            return ([state], precond,[numeric_effects])
    else:
        print('stack')
        print(state.clear[block1],state.clear[block2])
        print(block1,block2)
        return False


#backward or down
def unstack(state, block1, block2):
    state1=copy.copy(state)
    if state.agent[agent] in state.infront and state.clear[state.infront[loc]]:
        precond={'on':{block1:block2}}
        if ND:
            if not state.clear[state.behind[loc]]:
                return False
            precond['clear'][state.behind[loc]]=1
            return ([state,state1],precond)
        else:
            return ([state], precond)
    else:
        print('unstack')
        return False


treehop.declare_operators(stack, unstack)

def find_tallest(state):
    size=0
    top=None
    tempSize=0
    tempTop=None
    for block in state.clear:
        tempSize=0
        tempTop=block
        while block in state.on:
            tempSize+=1
            block=state.on[block]
        if tempSize>size:
            size=tempSize
            top=tempTop
    return size,top

        
def achieve_goal(state, n):
    size,top=find_tallest(state)
    n=n-size
    moves=[]
    used=[]
    energy=state.energy[1]
    for i in range(n):
        if energy<10:
            moves.append('recharge')
        block=choice([block for block in state.clear if state.clear[block] and block!=top and block not in used])
        if not state.clear[block]:
            print(str(block)+" IS NOT CLEAR")
        moves.append(('stack',block,top))
        energy-=10
        top=block
        used.append(block)
    return moves

treehop.declare_methods('achieve_goal',achieve_goal)



