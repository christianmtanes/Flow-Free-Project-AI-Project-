import time
import numpy
from variable import Variable
import math
import itertools
import Tests

''' gets in initial board and return a list of variables
 each variable represents a square in the board
'''
def setVariables(board):
    variables = []
    colors = allColors.copy()
    for i in range(len(board)):
        for j in range(len(board)):
            variables.append(Variable((i,j), board[i][j]))
            if(board[i][j] != '0' and board[i][j] not in colors):
                variables[i*len(board) + j].isTarget =True
            if(board[i][j] in colors):
                colors.remove(board[i][j])
                variables[i*len(board) + j].isSource =True        
    return variables


''' get a list of variables and prints it in a matrix form , each variable is printed and presented in the following format:
 (previous variable, color of square, next variable)
'''
def printvars(variables, length):
    for i in range(length):
        for j in range(length):
            if variables[i*length + j].isSource:
                if variables[i*length + j].next == None:
                    print(("s",variables[i*length + j].color, '-' ),end="",flush=True)
                else:
                    print(("s",variables[i*length + j].color, variables[i*length + j].next.position),end="",flush=True)
            elif variables[i*length + j].isTarget:
                if variables[i*length + j].previous == None:
                    print(("-",variables[i*length + j].color, "t"),end="",flush=True)
                else:
                    print((variables[i*length + j].previous.position, variables[i*length + j].color,"t"),end="",flush=True)
            else:
                if variables[i*length + j].previous == None and variables[i*length + j].next == None:
                    print (('-',variables[i*length + j].color, '-'),end="",flush=True)
                else:
                    print((variables[i*length + j].previous.position, variables[i*length + j].color,variables[i*length + j].next.position ),end="",flush=True)
            print(" ",end="",flush=True)
        print()
        
''' print a  board
'''
def printMatrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            print(matrix[i][j],end="",flush=True)
            print(" ",end="",flush=True)
        print()
'''
print a the variables in board format and only color of variables
'''
def printVarBoard(varBoard):
    for i in range(len(varBoard)):
        for j in range(len(varBoard)):
            print(varBoard[i][j].color,end="",flush=True)
            print(" ",end="",flush=True)
        print()

'''
constraints return true if an assiagnment fullfills the constraints
'''
def constraints(variable, value):
    
    # here the value is a suggested neighbor to be the source's 'next'
    if variable.isSource:
        # this is constraint on next in general value == next
        for neighbor in variable.getNeighbors():
            if neighbor.previous == variable and neighbor != value:
                
                return False
        if value.isTarget or (value.color != '0' and value.color != variable.color) or (value.color == variable.color and value.previous != None and value.previous != variable):
            return False
        return True
    # here the value is a suggested neighbor to be the target's 'previous'
    elif variable.isTarget:
        #this is constraint on previous in general
        for neighbor in variable.getNeighbors():
            if neighbor.next == variable and neighbor != value:
                return False
        if value.isSource or (value.color != '0' and value.color != variable.color) or (value.color == variable.color and   value.next != None and value.next != variable):
            return False
        return True
    # here the suggest value is a vector (neighbor for previous, color , neighbor for next)
    else:
        
        ##constraint on next (value[2])
        for neighbor in variable.getNeighbors():
            if neighbor.previous == variable and neighbor != value[2]:
                return False
        if  value[2].isSource or (value[2].color != '0' and value[2].color != value[1]) or (value[2].color == value[1] and value[2].previous != None and value[2].previous != variable):
            return False
        for neighbor in variable.getNeighbors():
            if neighbor.next == variable and neighbor != value[0]:
                return False
        ##constraint on previous (value[0])
        if  value[0].isTarget or (value[0].color != '0' and value[0].color != value[1]) or (value[0].color == value[1] and value[0].next != None and  value[0].next != variable):
            return False
        return True
'''
select a value to be assigned that is consistent
'''
def selectValue(variable):
    while(len(variable.legalValues) > 0):
        value =  variable.legalValues[0]
        variable.legalValues.remove(value)
        if constraints(variable, value): # value is consistent
            return value
    return None
'''
iterative backtracking algorithm for the csp problem.
'''
def backtrack(variables):
    i = 0
    variables[i].resetVariable()
    while(i >= 0 and i < len(variables)):
        value = selectValue(variables[i])
        if value == None:
            # backtracking
            variables[i].resetVariable()
            i -= 1
        else:
            # moving forward
            variables[i].setVariable(value)
            i += 1
            if i < len(variables):                
                variables[i].resetVariable()        
    if i < 0 :
        return None
    else:
        return variables

for game in Tests.all5X5games:
    allColors =  game[0]
    board = game[1]
    length = len(board)
    print("board to solve")
    printMatrix(board)
    variables = setVariables(board)

    # set the neighbor of each variable
    for var in variables:
        var.setNeighbors(variables,length)
        
    # set the the lagal values for each 
    for var in variables:
        var.setVarDomain(allColors)
        
    t0 = time.time()        
    variables = backtrack(variables)
    t1 = time.time() - t0
    print("----------solution-----------------")
    if variables == None:
        print("failure")
    else:
        for i in range(length):
                for j in range(length):
                    print(Variable.getVarByPos((i,j), variables).color,end="",flush=True)
                    print(" ",end="",flush=True)
                print()
    print("solution found after", t1, "seconds")
