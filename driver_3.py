# -*- coding: utf-8 -*-
"""
Created on Sat May 27 17:15:47 2017

@author: p_mal
"""

#Import packages
import sys
import queue
import timeit
#if sys.platform == "win32":
#    import psutil
#else:
#    import resource


#Imput variables
algorithm=sys.argv[1]
initialState=list(map(lambda x:int(x),sys.argv[2].split(",")))

#sanity check
if algorithm not in {"bfs","dfs","ast"}:
    print("please type in a valid algorithm: bfs, dfs or ast\n")
if set(initialState)==set(range(9)):
    board=True
else:
    print("invalid board, please type in a sequence of 9 numbers ranging from 0 to 9")
    board=False

goalState=list(range(9))

#Function to display boards
'''
def display(state):
    print("#######\n#{} {} {}#\n#{} {} {}#\n#{} {} {}#\n#######\n".format(state[0],
          state[1],state[2],state[3],state[4],state[5],state[6],state[7],state[8]))
'''

#Node Class
class Node:
    def __init__(self,state,parent,movement,depth,cost):
        self.state=state
        self.parent=parent
        self.movement=movement
        self.depth=depth
        if self.state==None:
            self.cost=0
        else:
            self.cost=self.manhattan()
    
    def __repr__(self):
        #display(self.state)
        return "\n#######\n#{} {} {}#\n#{} {} {}#\n#{} {} {}#\n#######\n".format(self.state[0],
          self.state[1],self.state[2],self.state[3],self.state[4],self.state[5],self.state[6],self.state[7],self.state[8]) #str(self.state)
    
    def get_neighbors(self,Frontier,Explored):
        neighbors=[]
        ind=self.state.index(0)
        neighbors.append(Node(empty_up(self.state,ind),self,"Up",self.depth+1,0))
        neighbors.append(Node(empty_down(self.state,ind),self,"Down",self.depth+1,0))
        neighbors.append(Node(empty_left(self.state,ind),self,"Left",self.depth+1,0))
        neighbors.append(Node(empty_right(self.state,ind),self,"Right",self.depth+1,0))
                
        neighbors=[n for n in neighbors if bool(n.state != None and tuple(n.state) not in Explored )]
        for n in neighbors:
            Explored.add(tuple(n.state))
        return neighbors
    
    def get_neighbors_ast(self, Frontier,Explored):
        neighbors=[]
        ind=self.state.index(0)
        neighbors.append(Node(empty_up(self.state,ind),self,"Up",self.depth+1,0))
        neighbors.append(Node(empty_down(self.state,ind),self,"Down",self.depth+1,0))
        neighbors.append(Node(empty_left(self.state,ind),self,"Left",self.depth+1,0))
        neighbors.append(Node(empty_right(self.state,ind),self,"Right",self.depth+1,0))
        _neighbors=[]       
        for n in neighbors:
            if n.state==None:
                continue
            elif tuple(n.state) in set(tuple(i.state) for i in Frontier):
                ind=[i.state for i in Frontier].index(n.state)
                Frontier[ind].cost=min(Frontier[ind].cost,n.cost)
                continue
            elif tuple(n.state) not in Explored:
                Explored.add(n)
                _neighbors.insert(0,n)    
        return _neighbors
    
    def manhattan(self):
        goalposition=[ (2, 1), (3, 1), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3)]
        initposition=[(self.state.index(i)%3+1,self.state.index(i)//3 +1) for i in range(1,9)]
        return sum(map(lambda x,y: abs(y[0]-x[0])+abs(y[1]-x[1]),goalposition,initposition))
    
    def __lt__(x,y):
        return bool(x.depth+x.cost<y.depth+y.cost)
        
    
#Definition of the valid movements
def empty_up(board,ind):
    if ind not in {0,1,2}:
        b=board[:]
        b[ind],b[ind-3]=b[ind-3],b[ind]
        return b

def empty_down(board,ind):
    if ind not in {6,7,8}:
        b=board[:]
        b[ind],b[ind+3]=b[ind+3],b[ind]
        return b

def empty_right(board,ind):
    if ind not in {2,5,8}:
        b=board[:]
        b[ind],b[ind+1]=b[ind+1],b[ind]
        return b

def empty_left(board,ind):
    if ind not in {0,3,6}:
        b=board[:]
        b[ind],b[ind-1]=b[ind-1],b[ind]
        return b  

########################################
#                                      #
#            SEARCH AGENTS             #
#                                      #
########################################

#Breadth-First Search (BFS)
def bfs(startState,endState):
    Frontier=[Node(startState,None,None,0,0)]
    Explored=set()
    response_string=""
    a=timeit.timeit()
    expand=0
    while len(Frontier)!=0:
        node=Frontier.pop(0)
        Explored.add(tuple(node.state))

        if node.state==endState:
            _node=node
            seq=[]
            while _node.depth!=0:
                seq.insert(0,_node.movement)
                _node=_node.parent
            response_string+="path_to_goal:"+str(seq)+"\n"
            response_string+="cost_of_path: "+str(len(seq))+"\n"
            response_string+="nodes_expanded:"+str(expand)+"\n"
            response_string+="search_depth:"+str(node.depth)+"\n"
            response_string+="max_search_depth:"+str(max([i.depth for i in Frontier]+[0]))+"\n"
            response_string+="running_time:"+str(timeit.timeit()-a)+"\n"
            #response_string+="max_ram_usage:"+str( psutil.Process().memory_info().rss)+"\n"
            
            return "----bfs----\n"+response_string+"Success\n"
        
        expand+=1
        for neighbor in node.get_neighbors(Frontier,Explored):
            Frontier.append(neighbor)

    return "----bfs----\n"+"Failure"

#Depth-First Search (DFS)
def dfs(startState,endState):
    Frontier=[Node(startState,None,None,0,0)]
    Explored=set()
    response_string=""
    a=timeit.timeit()
    expand=0
    while len(Frontier)!=0:
        node=Frontier.pop(0)
        Explored.add(tuple(node.state))

        if node.state==endState:
            _node=node
            seq=[]
            while _node.depth!=0:
                seq.insert(0,_node.movement)
                _node=_node.parent
            response_string+="path_to_goal:"+str(seq)+"\n"
            response_string+="cost_of_path: "+str(len(seq))+"\n"
            response_string+="nodes_expanded:"+str(expand)+"\n"
            response_string+="search_depth:"+str(node.depth)+"\n"
            response_string+="max_search_depth:"+str(max([i.depth for i in Frontier]+[0]))+"\n"
            response_string+="running_time:"+str(timeit.timeit()-a)+"\n"
            #response_string+="max_ram_usage:"+str( psutil.Process().memory_info().rss)+"\n"
            
            return "----dfs----\n"+response_string+"Success\n"
            return "Success"
        expand+=1
        _Frontier=node.get_neighbors(Frontier,Explored)
        _Frontier.extend(Frontier)
        Frontier=_Frontier
        
        
    return "----dfs----\n"+"Failure"

#A-star (AST)
def ast(startState,endState):
    Frontier=[Node(startState,None,None,0,0)]
    Explored=set()
    expand=0
    response_string=""
    a=timeit.timeit()
    while len(Frontier)!=0:
        
        Frontier=sorted(Frontier)
        
        node=Frontier.pop(0)
        Explored.add(tuple(node.state))

        if node.state==endState:
            _node=node
            seq=[]
            while _node.depth!=0:
                seq.insert(0,_node.movement)
                _node=_node.parent
            
            response_string+="path_to_goal:"+str(seq)+"\n"
            response_string+="cost_of_path: "+str(len(seq))+"\n"
            response_string+="nodes_expanded:"+str(expand)+"\n"
            response_string+="search_depth:"+str(node.depth)+"\n"
            response_string+="max_search_depth:"+str(max([i.depth for i in Frontier]+[0]))+"\n"
            response_string+="running_time:"+str(timeit.timeit()-a)+"\n"
            #response_string+="max_ram_usage:"+str( psutil.Process().memory_info().rss)+"\n"
            
            return "----ast----\n"+response_string+"Success\n"
        
        expand+=1
        for neighbor in node.get_neighbors_ast(Frontier,Explored):
            Frontier.insert(0,neighbor)

    return "----ast----\n"+"Failure"

if algorithm=="bfs" and board:
    s=bfs(initialState,goalState)
    f=open("output.txt","w")
    f.write(s)
    f.close()

if algorithm=="dfs" and board:
    s=dfs(initialState,goalState)
    f=open("output.txt","w")
    f.write(s)
    f.close()
    
if algorithm=="ast" and board:
    s=ast(initialState,goalState)
    f=open("output.txt","w")
    f.write(s)
    f.close()
    
print("Done. Please look at output file")
    

