# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 16:20:38 2017

@author: p_mal
"""
from random import randint
from BaseAI import BaseAI
from math import log
from math import fabs
import time

class PlayerAI(BaseAI):
    
    def __init__(self):
        self.time_limit=0
           
    def getMove(self, grid):
        self.time_limit=time.clock()+0.2
        result=(0,None)
        
        result=self.maximize(grid,float("-inf"),float("inf"),1)
            
        return result[1]
        
    def maximize(self,grid,alpha,beta,depth):
        moves=grid.getAvailableMoves()
        maxmove=-1
        maxutility=float("-inf")
        if depth>5 or not grid.canMove() or time.clock()>self.time_limit:
                return (self.heuristic(grid),None)
        
        for move in moves:
            newgrid=grid.clone()
            newgrid.move(move)
            
            result=self.minimize(newgrid,alpha,beta,depth+1)
            
            if result[0]>maxutility:
                maxmove=move
                maxutility=result[0]
            if maxutility>=beta:
                break
            if maxutility>alpha:
                alpha=maxutility
                
        return (maxutility,maxmove)
     
    def minimize(self,grid,alpha,beta,depth):
        cells=grid.getAvailableCells()
        minutility=float("inf")
        if depth>5 or not grid.canMove() or time.clock()>self.time_limit:
                return (self.heuristic(grid),None)
        
        result=[float("inf"),None]
        
        for cell in cells:
            newgrid=grid.clone()
            newgrid.insertTile(cell,self.NewTileValue())
            
            result=self.maximize(newgrid,alpha,beta,depth+1)
            
            if result[0]<minutility:
                minutility=result[0]
            if minutility<=alpha:
                break
            if minutility<beta:
                beta=minutility
                
        return (minutility,-1)       
                
    def NewTileValue(self):
        NewTileValue = [2, 4]
        probability= 0.9
        
        if randint(0, 99) < 100 * probability: 
            return NewTileValue[0] 
        else: 
            return NewTileValue[1]
            
    def heuristic(self,grid):
        #emptycells        
        emptycells=len(grid.getAvailableCells())
        #maxtile
        maxtile=grid.getMaxTile()
        
        #score, smoothness and monotocity
        score=0
        smoothness=0
        monotocity=0
        weights=[[6,5,4,3],[5,4,3,2],[4,3,2,1],[3,2,1,0]]
        
        for i in range(4):
            for j in range(4):
                score+=grid.map[i][j]*weights[i][j]
                
        
        for i in range(4):
            for j in range(3):
                if grid.map[i][j]>=grid.map[i][j+1] and grid.map[i][j]!=0:
                    monotocity+=log(grid.map[i][j],2)
                if grid.map[j][i]>=grid.map[j+1][i] and grid.map[j][i]!=0:
                    monotocity+=log(grid.map[j][i],2)
                if grid.map[i][j]==grid.map[i][j+1] and grid.map[i][j]!=0:
                    smoothness+=log(grid.map[i][j],2)
                if grid.map[j][i]==grid.map[j+1][i] and grid.map[j][i]!=0:
                    smoothness+=log(grid.map[j][i],2)
        
        return 0.5*emptycells+10*log(maxtile,2)+0.2*monotocity+2*smoothness+score


           
       
    

        
        
        
        
            
            
            
