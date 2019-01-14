#Use to run plans
import json
P=__import__('AP')#substitute problem file here
D=__import__('AD')#substitue domain file here
import treehop as T#import Planner
from random import *
from importlib import reload
import copy
from datetime import datetime
import sys
import time
state=copy.deepcopy(P.state)#gets starting state from problem file
reqP=.5#required percentage for expectations to be true
counter=0#keeps track of actions taken
countFailed=0#keeps track of replans
clear=copy.deepcopy(P.state.clear)#all clear copy
print(P.n)
def check(state,exp):
    global reqP
    off=0
    if isinstance(exp,T.State):
        return T.eq_state(state,exp)
    for d in exp:
        for e in exp[d]:
            if isinstance(exp[d][e],dict):
                for p in exp[d][e]:
                    if e not in getattr(state,d):
                        #print('1',d,e)
                        return False
                    if not getattr(state,d)[e]==p:
                        if exp[d][e][p]>=reqP:
                            #print('2',d,e,exp[d][e],getattr(state,d)[e])
                            return False
            else:
                if not getattr(state,d)[e]==exp[d][e]:
                    #print('3',d,e,exp[d][e],getattr(state,d)[e])
                    return False
    return True
placed=[]
#take plan and run it
def runPlan(tree,exp):
    global placed
    global counter
    global countFailed
    global state
    global clear
    #print(tree.action,tree.cond)
    for b in state.lit:
        if state.lit[b]==2:
            state.score[b]=state.score[b]+1
    if tree.action=='Finished':
        #print(getattr(tree,exp))
        if not check(state,getattr(tree,exp)):
            print('failed final expect')
            pass
        else:
            print('passed final expect')
            pass
        #print(getattr(tree,exp)
        for x in range(P.start,P.end+1):
            if not state.score[x]==0:
                counter+=state.score[x]
        return
    returnval=getattr(D,tree.action)(state,*tree.cond)
    if not returnval:
        returnval=getattr(D,tree.action)(state,*tree.cond)
        for d in treeFexp:
            for e in tree.Fexp[d]:
                if isinstance(tree.Fexp[d][e],dict):
                    for p in tree.Fexp[d][e]:
                        tree.Fexp[d][e]=p
        print('bad retval',tree.action,tree.cond)
        print('on',state.on)
        tree=newplan(tree.Fexp)
        runPlan(tree,exp)
        return
    states=returnval[0]
    x=randint(0,len(states)-1)
    #print('x',x)
    state=copy.deepcopy(states[x])
    change={}
    if not tree.action == "Finished":
        b=randint(0,P.blocks-1)
        state.lit[b]=2
    expect={}
    if not x==0 and (check(copy.deepcopy(state),getattr(tree.branch[x-1].next,exp))):
        #print('1')
        runPlan(tree.branch[x-1].next,exp)
        return
    elif not x==0:
        expect=getattr(tree.branch[x-1].next,exp)
        #print('1expect')#,tree.branch[x-1].next.Fexp)
    if x==0 and tree.branch and check(copy.deepcopy(state),getattr(tree.next.next,exp)):
        #print('2')
        runPlan(tree.next.next,exp)
        return
    elif x==0 and tree.branch:
        expect=getattr(tree.next.next,exp)
        #print('2expect',expect)
        #print('2')#,tree.next.next.num,tree.next.next.action,tree.next.next.Fexp)
    if not tree.branch and check(copy.deepcopy(state),getattr(tree.next,exp)):
        #print('3')
        runPlan(tree.next,exp)
        return
    elif not tree.branch:
        expect=getattr(tree.next,exp)
        #print('3expect',tree.next.Fexp)
        #PASS THE ENVIRONMENT CHANGE THAT FORCED REPLANNING
    Fexp=copy.deepcopy(expect)
    #print('usedExpect',expect)
    if not exp=='state':
        #print('expect',expect)
        remove={}
        for d in expect:
            if d=='lit':
                pass
                #print(d)
                #print(getattr(state,d))
                #print(expect[d])
            for e in expect[d]:
                if isinstance(expect[d][e],dict):
                    for p in expect[d][e]:
                        if e not in getattr(state,d):
                            if d not in remove:
                                remove[d]=[]
                            #print('add to remove',d,e)
                            #print(getattr(state,d))
                            #print(expect[d][e])
                            remove[d].append(e)
                            pass
                        elif not getattr(state,d)[e]==p:
                            #print('update',d,e,getattr(state,d)[e],expect[d][e][p])
                            if expect[d][e][p]>=reqP:
                                Fexp[d][e]=getattr(state,d)[e]
                else:
                    if not getattr(state,d)[e]==expect[d][e]:
                        Fexp[d][e]=getattr(state,d)[e]
        for d in remove:
            for e in remove[d]:
                if e in Fexp[d]:
                    Fexp[d].pop(e)
        remove={}
        for d in Fexp:
            for e in Fexp[d]:
                if isinstance(Fexp[d][e],dict):
                    for p in Fexp[d][e]:
                        Fexp[d][e]=p
        tree=newplan(Fexp)
        runPlan(tree,exp)
        return
    return
runs=5
problems=5
goals={'on':{},'lit':{}}
for x in range (P.start,P.end):
    goals['on'][x]={x+1:1}
for x in range (P.start,P.end+1):
    goals['lit'][x]={0:1}
    pass
#goals={'on':{19:{20:1},18:{19:1},17:{18:1},16:{17:1},15:{16:1},14:{15:1},13:{14:1},12:{13:1},11:{12:1},10:{11:1}}}
#goals={'lit':{'B1':{1:1},'B2':{1:1},'B3':{1:1}}}
print(goals)
Exp=['Fexp','Bexp','oBexp','Rexp']
#Exp=['Fexp']
tests=['time','scores','fail']

def newplan(exp):
    global countFailed
    methods=T.methods
    operators=T.operators
    State=T.State
    reload(T)
    T.State=State
    T.methods=methods
    T.operators=operators
    T.stateList={}
    temp=[]
    #print('exp',exp)
    for b in exp['lit']:
        if exp['lit'][b]==2 and state.lit[b]==2:
            temp.append(b)
    temp=[('POF',temp)]
    for g in P.goals:
        temp.append(g)
    tree=T.wrapper(copy.deepcopy(state),temp,Fexp=exp)
    #T.print_plan(tree,exp='Fexp')
    return tree    

def replan():
    methods=T.methods
    operators=T.operators
    reload(T)
    T.methods=methods
    T.operators=operators
    global placed
    placed=[]
    global state
    state=copy.deepcopy(P.state)

def reset():
    print('setting up new problem')
    replan()
    success=0
    while not success:
        #try:
        reload(P)
        success=1
        #except:
        pass
    global state
    state=copy.deepcopy(P.state)
threads=0
results={}
def solve(x,top):
    data=top[x][0]
    for key in tests:
        data[key]={}
    global counter
    global Exp
    global goals
    global runs
    global placed
    global state
    print('this is problem',x)
    reset()
    for exp in Exp:
        for key in tests:
            data[key][exp]={}
        counter=0
        countFailed=0
        a = datetime.now()
        for y in range(0,runs):
            print(x,exp, y)
            placed=[]
            state=copy.deepcopy(P.state)
            success=0
            tc=counter
            tcf=countFailed
            success=0
            while not success:
                try:
                    #T.print_plan(P.Plan,exp=exp)
                    runPlan(P.Plan,exp)
                    success=1
                except:
                    counter=tc
                    countFailed=tcf
                    replan()
            #print(goals)
            #print(state.on,state.lit)
            if not check(state,goals):
                print('here')
                print(state.on)
                print(state.lit)
                time.sleep(1)
                countFailed+=1
        b=datetime.now()
        data['fail'][exp]=(countFailed/runs)*100
        data['time'][exp]=((b-a)/runs).total_seconds()
        data['scores'][exp]=counter/runs
    top[x][0]=data
from multiprocessing import Process,Manager
manager=Manager()
top=manager.list(range(0,problems))
for x in range(0,problems):
    li=manager.list()
    li.append({})
    top[x]=li
jobs=[]
for x in range(0,problems):
    p=Process(target=solve,args=(x,top))
    jobs.append(p)
    p.start()
    time.sleep(.5)
for p in jobs:
    p.join()
data={}
for x in range(0,len(top)):
    data[x]=top[x][0]
with open("A2ExpData.txt","w+") as f:
    json.dump(data,f)
#print('Regression:',Rexp)

