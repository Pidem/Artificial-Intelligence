# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 16:48:08 2017

@author: p_mal

"""
import sys
from copy import deepcopy

#List of all the cells in the puzzle
celllist=list((i+str(j) for i in ["A","B","C","D","E","F","G","H","I"] for j in range(9)))


##########################################
#   Sudoku class and support functions   #
##########################################

#the block function returns an integer that corresponds to the block that the 
#given cell is part of (top left is block 1, bottom right is block 9)

def block(cell):
    row=cell[0]
    col=int(cell[1])
    if row in {'A','B','C'}:
        if col<3:
            return 1
        elif col<6:
            return 2
        else: 
            return 3
    elif row in {'D','E','F'}:
        if col<3:
            return 4
        elif col<6:
            return 5
        else: 
            return 6
    else:
        if col<3:
            return 7
        elif col<6:
            return 8
        else: 
            return 9


#the neighbor function returns a list with all the neighboringcells 
#it is used to get all the constraints  

def getneighbors(cell):
    r=set()
    b=block(cell)
    for k in celllist:
        if str(k)==str(cell):
            pass
        if (k[0] in cell) or (k[1] in cell):
            r.add(k)
        if block(k)==b:
            r.add(k)
        r.discard(cell)
    return sorted(list(r))
    
#The Class Sudoku stores the input grid used to display, printing methods, and 
#most importantly the csp: the csp is a dictionary:
#  keys= cell coordinates (for example 'A0')
#  values= list of length 3: [assigned value, domain, constrained cells]    
    
class Sudoku:
    def __init__(self,grid):
        self.csp=dict((celllist[i],[grid[i],[int(grid[i])] if int(grid[i])!=0 else [1,2,3,4,5,6,7,8,9],getneighbors(celllist[i])]) for i in range(81))
        
    def __repr__(self):
        count=1
        rep=""
        for c in celllist:
            rep+=str(self.csp[c][0])
            if count%3==0:
                rep+="|"
                if count%9==0:
                    rep+="\n"
                    if count%27==0:
                        rep+="---+---+----\n"
            count+=1
        return rep
    
    def issolved(self):
        unassigned=0        
        for c in celllist:
            if len(self.csp[c][1])>1:
                unassigned+=1
        
        if not unassigned:
            for c in celllist:
                self.csp[c][0]=self.csp[c][1][0]
        return unassigned
    
##########################################
# AC3methods using only arc constraints  #
########################################## 

#The AC3 function makes the csp arc consistent and removes the non-authorized
#values given the assigned values    
    
def AC3(Sudoku):
    queue=[(i,j) for i in celllist for j in Sudoku.csp[i][2]]
    
    while bool(queue):
        Xi,Xj=queue.pop()
        if Revise(Sudoku,Xi,Xj):
            if len(Sudoku.csp[Xi][1])==0:
                return False
            for n in getneighbors(Xi):
                if n!=Xj:
                    queue.append((n,Xi))
    return True

def Revise(Sudoku, Xi,Xj):
    revised=False
    di=Sudoku.csp[str(Xi)][1]
    for x in di:
        if not bool(set(Sudoku.csp[Xj][1])-{x}):
            Sudoku.csp[str(Xi)][1].remove(x)                
            revised=True              
    return revised  
    
#Backtracking Function 

def Select_Unassigned_Variable(Sudoku,assignment):
    sel_cell='A0'
    min_d=10   
    for c in celllist:
        if len(Sudoku.csp[c][1])>1 and c not in assignment.keys():
            if len(Sudoku.csp[c][1])<min_d:
                min_d=len(Sudoku.csp[c][1])
                sel_cell=c
    return sel_cell

#Implementation of the Backtrack algorithm with Inference (look-forward implem.)

def Order_Domain_Values(var,assignment,Sudoku):
    values=[]
    for val in Sudoku.csp[var][1]:
        values.append((val,sum([Sudoku.csp[c][1].count(val) for c in celllist])))
    return [i[0] for i in sorted(values, key=lambda x:x[1])]
    
def CompleteAssignment(Sudoku,assignment):
    for c in celllist:
        if len(Sudoku.csp[c][1])!=1 and c not in assignment.keys():
            return False
    return True

def ConsistentAssignment(assignment,variable,value,Sudoku):
    for c in Sudoku.csp[variable][2]:
        try:     
            if assignment[c]==value:
                return False
        except:
            pass
    return True

def GetAssignedVariables(Sudoku):
    assignment={}
    for c in celllist:
        if len(Sudoku.csp[c][1])==1:
            assignment[c]=Sudoku.csp[c][1][0]
    return assignment

def Inference(Sudoku,var,value,assignment):
    inferences={}
    
    neighbors=getneighbors(var)
    
    for n in neighbors:
        
        if value in Sudoku.csp[n][1]:    
            Sudoku.csp[n][1].remove(value)
            if len(Sudoku.csp[n][1])==0:
                return False
            
            elif len(Sudoku.csp[n][1])==1:
                inferences[n]=Sudoku.csp[n][1][0]
                if Inference(Sudoku,n,Sudoku.csp[n][1][0],assignment)==False:
                    return False
    return inferences

def Backtrack(assignment,Sudoku):
    if CompleteAssignment(Sudoku,assignment):
        return assignment
        
    var = Select_Unassigned_Variable(Sudoku,assignment)
    
    temp_sudoku=deepcopy(Sudoku.csp)
    
    domain=deepcopy(Sudoku.csp[var][1])
    for value in Order_Domain_Values(var,assignment,Sudoku):
#        print(var,value)
        if ConsistentAssignment(assignment,var,value,Sudoku):
            
            assignment[var]=value
            
            inferences=Inference(Sudoku,var,value,assignment)
            
            if isinstance(inferences,dict):
                assignment.update(inferences)
                result=Backtrack(assignment,Sudoku)
                
                if isinstance(result,dict):
                    return result
                    
            assignment.pop(var,None)
            
            if isinstance(inferences,dict):
                for key in inferences.keys():
                    assignment.pop(key)
  
        Sudoku.csp=deepcopy(temp_sudoku)
         
    return False

#g=Sudoku("003020600900305001001806400008102900700000008006708200002609500800203009005010300")
#print(g)
#_a=g.issolved()
#AC3(g)
#while g.issolved()!=_a:
#    _a=g.issolved()
#    AC3(g)
#Backtrack({},g)
#g.issolved()
#print(g)


if __name__ == '__main__':
    inputgrid=str(sys.argv[1])
    g=Sudoku(inputgrid)
    print(g)
    _a=g.issolved()
    AC3(g)
    while g.issolved()!=_a:
        _a=g.issolved()
        AC3(g)
    try:
        Backtrack({},g)
    except:
        print("Error 404")
    g.issolved()
    r=""
    for c in celllist:
        r+=str(g.csp[c][0])
    text_file = open("output.txt", "w")
    text_file.write(r)
    print("Done")

#if __name__ == '__main__' :
#    import time
#    import pandas as pd
#    
#    #import all the puzzles from input file
#    
##    inputfile=str(sys.argv[1])
##    f = open(inputfile,"r")
#    f = open("C:/Users/p_mal/Documents/Columbia/Courses/Artificial Intelligence/Assignments/assignment4/assignment4/sudokus_start.txt", "r")
#    sudokuList = f.read()
#    sudokus=[]
#    for line in sudokuList.split("\n"):
#        if len(line)==81:
#            sudokus.append(line)
#    
#    output=[]
#    n=1
#    for s in sudokus:
#        print("computing grid",n)
#        g=Sudoku(s)
#        starttime=time.clock()        
#        _a=g.issolved
#        AC3(g)
#        
#        while g.issolved()!=_a:
#            _a=g.issolved()
#            AC3(g)
#        if g.issolved()==0:
#            ac3_status="solved"
#        else:
#            ac3_status="non solved"
#        ac3_time=time.clock()-starttime
#        
#        Backtrack({},g)
#        if g.issolved()==0:
#            bt_status="solved"
#        else:
#            bt_status="non solved"
#        bt_time=time.clock()-ac3_time
#        
##        g=Sudoku(s)
##        Backtrack({},g)
##        if g.issolved()==0:
##            bt2_status="solved"
##        else:
##            bt2_status="non solved"
##        bt2_time=time.clock()-bt_time
#        
#        output.append([n,ac3_status,ac3_time,bt_status,bt_time])
#        
#        n+=1
#     

        





