#variable.py

# class for a variable, the variable is a square in the game board
# it will contain the variable legal values
import math
import itertools

class Variable:
    
    def __init__(self, position, color):
        self.position = position # a tuple (row, col)
        self.color = color # '0' if no assignment yet
        self.domain = None
        self.legalValues = []
        self.isSource =False# current legal values for this variable, initialized as the domain
        self.isTarget =False
        self.neighbors = [] # neighbors of this variable
        self.next = None #  the next var in the path.
        self.previous = None # the previos variable in the path.
        
    '''
    reset the variable's domain.
    '''
    def resetVariable(self):
        self.legalValues = self.domain.copy()
        if not(self.isTarget or self.isSource):
            self.color = '0'
        self.next = None
        self.previous = None
       

    def setVariable(self, value):
        if self.isSource:
            self.next = value
        elif self.isTarget:
            self.previous = value
        else :
            self.previous = value[0]
            self.color = value[1]
            self.next = value[2]
    ''' gets the variable by its original position  in board
        static method
    '''
    def getVarByPos( position, variables):
        for var in variables:
            if var.position == position:
                return var
            
    def setNeighbors(self, variables, length):
        if self.position[1]+1 < length:
            self.neighbors.append(Variable.getVarByPos((self.position[0],self.position[1] + 1),variables))
            
        if self.position[0]+1 < length:
            self.neighbors.append(Variable.getVarByPos((self.position[0]+1,self.position[1]),variables))
            
        if self.position[1]-1>= 0:
            self.neighbors.append(Variable.getVarByPos((self.position[0],self.position[1] - 1),variables))
        
        if self.position[0]-1 >= 0:
            self.neighbors.append(Variable.getVarByPos((self.position[0]-1,self.position[1]),variables))
    
    def getNeighbors(self):
        return self.neighbors
    
    def isAssigned(self):
        if self.isTarget:
            return self.previous != None
        if self.isSource:
            return self.next !=None
        return self.color != '0'
        
    def NumUnassignedNeighbors(self):
        count=0
        for neighbor in self.getNeighbors():
            if neighbor.isSource and neighbor.next == None:
                count += 1
            elif neighbor.isTarget and neighbor.previous == None:
                count += 1
            elif neighbor.color == '0':
                count +=1
        return count
            
    # for a regular variable , its domain is a vector , (previos, color , next)
    #for a source we only assign what is its next variable, so its domain is the neighbors of the variable
    # for a Target we only assign what is its previous variable, so its domain is the neighbors of the variable
    # gets all colors
    def setVarDomain(self, allcolors):
        neighbors = self.getNeighbors()
        if(self.isSource):
            domain = neighbors # the possiblitites is only on the next neighbor to go to not the color.
                               # the assignment is only on what is the next variable , color is already assigned, and no previous for this variable
        elif(self.isTarget):
            domain = neighbors # possibilities is only on the previous neighbor not color
        else:
            domain = list(itertools.product(neighbors, allcolors, neighbors))# cartesian product of neighborsXallcolorsXneighbors
            domain =  [d for d in domain if d[0] != d[2]] # removing a value the has previous == next because it is meaningless
        self.domain = domain
    ##  get the domain of the variable.    
    def getVarDomain(self):
        return self.domain
    
    #print the domain of the variable used for debugging
    def printDomain(self):
        if self.isSource:
            for val in self.legalValues:
                print(val.position)
            
        elif self.isTarget:
            for val in self.legalValues:
                print(val.position )
        else:
            for val in self.legalValues:
                print((val[0].position,val[1],val[2].position))
                
    # print the variable   
    def printVar(self):
        print(self.position)
        if self.isSource:
            print(self.next.position)
        if self.isTarget:
            print(self.previous.position)
        else:
            print(self.previous.position,self.color,self.next.position)
    def getIndex(self):
        return self.position[0]*numberOfvariables + self.position[1]
    
    def LegalValuesOfNeighbors(self):
        count = 0 
        for neighbor in self.getNeighbors():
            count += len(neighbor.legalValues)
        return count



        
