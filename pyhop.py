"""
Pyhop, version 1.2.2 -- a simple SHOP-like planner written in Python.
Author: Dana S. Nau, 2013.05.31

Copyright 2013 Dana S. Nau - http://www.cs.umd.edu/~nau

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   
Pyhop should work correctly in both Python 2.7 and Python 3.2.p
For examples of how to use it, see the example files that come with Pyhop.

Pyhop provides the following classes and functions:

- foo = State('foo') tells Pyhop to create an empty state object named 'foo'.
  To put variables and values into it, you should do assignments such as
  foo.var1 = val1

- bar = Goal('bar') tells Pyhop to create an empty goal object named 'bar'.
  To put variables and values into it, you should do assignments such as
  bar.var1 = val1

- print_state(foo) will print the variables and values in the state foo.

- print_goal(foo) will print the variables and values in the goal foo.

- declare_operators(o1, o2, ..., ok) tells Pyhop that o1, o2, ..., ok
  are all of the planning operators; this supersedes any previous call
  to declare_operators.

- print_operators() will print out the list of available operators.

- declare_methods('foo', m1, m2, ..., mk) tells Pyhop that m1, m2, ..., mk
  are all of the methods for tasks having 'foo' as their taskname; this
  supersedes any previous call to declare_methods('foo', ...).

- print_methods() will print out a list of all declared methods.

- pyhop(state1,tasklist) tells Pyhop to find a plan for accomplishing tasklist
  (a list of tasks), starting from an initial state state1, using whatever
  methods and operators you declared previously.

- In the above call to pyhop, you can add an optional 3rd argument called
  'verbose' that tells pyhop how much debugging printout it should provide:
- if verbose = 0 (the default), pyhop returns the solution but prints nothing;
- if verbose = 1, it prints the initial parameters and the answer;
- if verbose = 2, it also prints a message on each recursive call;
- if verbose = 3, it also prints info about what it's computing.
"""

#####TODO: AHA CONTINUOUS EFFECTS

# Pyhop's planning algorithm is very similar to the one in SHOP and JSHOP
# (see http://www.cs.umd.edu/projects/shop). Like SHOP and JSHOP, Pyhop uses
# HTN methods to decompose tasks into smaller and smaller subtasks, until it
# finds tasks that correspond directly to actions. But Pyhop differs from 
# SHOP and JSHOP in several ways that should make it easier to use Pyhop
# as part of other programs:
# 
# (1) In Pyhop, one writes methods and operators as ordinary Python functions
#     (rather than using a special-purpose language, as in SHOP and JSHOP).
# 
# (2) Instead of representing states as collections of logical assertions,
#     Pyhop uses state-variable representation: a state is a Python object
#     that contains variable bindings. For example, to define a state in
#     which box b is located in room r1, you might write something like this:
#     s = State()
#     s.loc['b'] = 'r1'
# 
# (3) You also can define goals as Python objects. For example, to specify
#     that a goal of having box b in room r2, you might write this:
#     g = Goal()
#     g.loc['b'] = 'r2'
#     Like most HTN planners, Pyhop will ignore g unless you explicitly
#     tell it what to do with g. You can do that by referring to g in
#     your methods and operators, and passing g to them as an argument.
#     In the same fashion, you could tell Pyhop to achieve any one of
#     several different goals, or to achieve them in some desired sequence.
# 
# (4) Unlike SHOP and JSHOP, Pyhop doesn't include a Horn-clause inference
#     engine for evaluating preconditions of operators and methods. So far,
#     I've seen no need for it; I've found it easier to write precondition
#     evaluations directly in Python. But I could consider adding such a
#     feature if someone convinces me that it's really necessary.
# 
# Accompanying this file are several files that give examples of how to use
# Pyhop. To run them, launch python and type "import blocks_world_examples"
# or "import simple_travel_example".


from __future__ import print_function
import copy,sys, pprint

############################################################
# States and goals
class Action():
    def __init__(self,name="Default",state=None):
        self.name=name
        self.children=[]
        self.effects=[]
        self.precond={}
        self.state=state
counter=0
class State():
    """A state is just a collection of variable bindings."""
    """NEED TO BE ALL DICTIONARIES"""
    def __init__(self,name):
        global counter
        self.__name__ = name
        self._num=counter
        counter+=1
    def get_diff(self,otherState):
        diff={}
        def addDiff(attr,var,val):
            if attr not in diff:
                diff[attr]={}
            diff[attr][var]=val
        for attr in vars(self):
            if attr[0]=="_":
                continue
            for var in getattr(self,attr):
                val=getattr(self,attr)[var]
                if var not in getattr(otherState,attr) or getattr(otherState,attr)[var]!=val:
                    addDiff(attr,var,val)
    def __eq__(self, otherState):
        for attr in vars(self):
            if attr[0]=="_":
                continue
            for var in getattr(self,attr):
                val=getattr(self,attr)[var]
                if var not in getattr(otherState,attr) or getattr(otherState,attr)[var]!=val:
                    return False
        return True
    def __hash__(self):
        return self._num
    def __copy__(self):
        global counter
        newstate=copy.deepcopy(self)
        newstate._num=counter
        counter+=1
        return newstate

class Goal():
    """A goal is just a collection of variable bindings."""
    def __init__(self,name):
        self.__name__ = name


### print_state and print_goal are identical except for the name

def print_state(state,indent=4):
    """Print each variable in state, indented by indent spaces."""
    if state != False:
        for (name,val) in vars(state).items():
            if name != '__name__':
                for x in range(indent): sys.stdout.write(' ')
                sys.stdout.write(state.__name__ + '.' + name)
                print(' =', val)
    else: print('False')

def print_goal(goal,indent=4):
    """Print each variable in goal, indented by indent spaces."""
    if goal != False:
        for (name,val) in vars(goal).items():
            if name != '__name__':
                for x in range(indent): sys.stdout.write(' ')
                sys.stdout.write(goal.__name__ + '.' + name)
                print(' =', val)
    else: print('False')

def print_plan_dfs(action, tab=0): #Needs work,incorrect
    for x in range(0,tab):
        print("    ",end="")
    print(action.name,action.children)
    first=0
    for child in action.children:
        print_plan_dfs(child, tab=tab + first)
        if first==0:
            first=1

############################################################
# Helper functions that may be useful in domain models

def forall(seq,cond):
    """True if cond(x) holds for all x in seq, otherwise False."""
    for x in seq:
        if not cond(x): return False
    return True

def find_if(cond,seq):
    """
    Return the first x in seq such that cond(x) holds, if there is one.
    Otherwise return None.
    """
    for x in seq:
        if cond(x): return x
    return None

############################################################
# Commands to tell Pyhop what the operators and methods are

operators = {}
methods = {}
goals = []

def declare_goals(goal_list):
    for goal in goal_list:
        goals.append(goal)
    return

def declare_operators(*op_list):
    """
    Call this after defining the operators, to tell Pyhop what they are. 
    op_list must be a list of functions, not strings.
    """
    operators.update({op.__name__:op for op in op_list})
    return operators

def declare_methods(task_name,*method_list):
    """
    Call this once for each task, to tell Pyhop what the methods are.
    task_name must be a string.
    method_list must be a list of functions, not strings.
    """
    methods.update({task_name:list(method_list)})
    return methods[task_name]

############################################################
# Commands to find out what the operators and methods are

def print_operators(olist=operators):
    """Print out the names of the operators"""
    print('OPERATORS:', ', '.join(olist))

def print_methods(mlist=methods):
    """Print out a table of what the methods are for each task"""
    print('{:<14}{}'.format('TASK:','METHODS:'))
    for task in mlist:
        print('{:<14}'.format(task) + ', '.join([f.__name__ for f in mlist[task]]))

############################################################
# The actual planner

edges=[]
verticies=[]
Policy={}
def pyhopT(state,tasks,depth=0):
    if depth>=10:
        return False,None
    """
    Try to find a plan that accomplishes tasks in state. 
    If successful, return the plan. Otherwise return False.
    """
    start=Action()#plan header node
    result = seek_plan(state,tasks,depth,start) #result holds True or False if planner succeeds or fails
    start.edges=edges
    start.verticies=verticies
    return result,start

def seek_plan(state,tasks,depth=0,prev_action=None):
    for oldstate in verticies:
        if oldstate==state:
            return True
    """
    Workhorse for pyhop. state and tasks are as in pyhop.
    - plan is the current partial plan.
    - depth is the recursion depth, for use in debugging
    - verbose is whether to print debugging messages
    """
    if tasks == []:
        return True
    task1 = tasks[0]
    if task1[0] in operators:
        verticies.append(state)
        operator = operators[task1[0]]
        opreturn= operator(copy.copy(state),*task1[1:])
        newstates=opreturn[0]
        newstate=newstates[0]
        if len(newstates)>1:
            otherstates=newstates[1:]
        else:
            otherstates=[]
        precond=opreturn[1]
        action=Action(name=task1, state=state)
        action.precond=precond
        edges.append((state,action))
        if newstate:
            edges.append((action,newstate))
            prev_action.children.append(action)
            action.effects.append(newstate.get_diff(state))
            solution = seek_plan(newstate,tasks[1:],depth,prev_action=action)
        for otherstate in otherstates:
            result,plan=pyhopT(otherstate,goals,depth+1)
            if result:
                action.children.append(plan.children[0])
                action.effects.append(otherstate.get_diff(state))
                edges.append((action, otherstate))
        if len(newstates)>0:
            if solution!=False:
                return True
    if task1[0] in methods:
        relevant = methods[task1[0]]
        for method in relevant:
            subtasks = method(state,*task1[1:])
            # Can't just say "if subtasks:", because that's wrong if subtasks == []
            if subtasks != False:
                solution = seek_plan(state,subtasks+tasks[1:],depth,prev_action=prev_action)
                if solution != False:
                    return True
    return False
