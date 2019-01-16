# TreeHop
Code for TreeHop planner and expectations
Check testP for example Problem file
Check testD for example Domain file. 
To use, run any problem file (python testP.py), make sure the problem file imports both the domain and Treehop.
Return value from Treehop.pyhop_t is a diction of states, one of which being the state given at the beginning call. 
All states have an associated expectation set, check that against return val applying an action to a state to determine next action to use
