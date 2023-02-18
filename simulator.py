import random
import math
from matplotlib import pyplot as plt
import numpy as np

def image_example():
    '''should produce red,purple,green squares
    on the diagonal, over a black background'''
    # RGB indexes
    red,green,blue = range(3)
    # img array 
    # all zeros = black pixels
    # shape: (150 rows, 150 cols, 3 colors)
    img = np.zeros((150,150,3))
    for x in range(50):
        for y in range(50):
            # red pixels
            img[x,y,red] = 1.0
            # purple pixels
            # set 3 color components 
            img[x+50, y+50,:] = (.5,.0,.5)
            # green pixels
            img[x+100,y+100,green] = 1.0
    plt.imshow(img)

def normpdf(x, mean, sd):
    """
    Return the value of the normal distribution 
    with the specified mean and standard deviation (sd) at
    position x.
    You do not have to understand how this function works exactly. 
    """
    var = float(sd)**2
    denom = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom

def pdeath(x, mean, sd):
    start = x-0.5
    end = x+0.5
    step =0.01    
    integral = 0.0
    while start<=end:
        integral += step * (normpdf(start,mean,sd) + normpdf(start+step,mean,sd)) / 2
        start += step            
    return integral    
    
recovery_time = 4 # recovery time in time-steps
virality = 0.2    # probability that a neighbor cell is infected in 
                  # each time step                                                  

class Cell(object):
    #has attributes x, y, and current state of the cell as a string
    def __init__(self,x, y):
        self.x = x
        self.y = y 
        self.state = "S" # can be "S" (susceptible), 
                         #"R" (resistant = dead), or 
                         # "I" (infected)
        #add a counter to remember how long each cell has been in state "I"
        self.count = 0
        
    def infect(self):
        #when called, state attribute needs to be set to "I"
        self.state = "I"
    
    def process (self, adjacent_cells):
        #method only relevant if the status of the cell is "I"
        if self.state == "I":
            self.count += 1
            if self.count > recovery_time:
                self.state = "S"
                return
            #used to see if a cell dies or not (probability)
            death = random.random()
            p_death = normpdf(self.count, 1, 0.5)
           
            if death > p_death:
                self.state = "R"
                return
            
            for cell in adjacent_cells:
                if cell.state == "S":
                    ran = random.random()
                    if ran < virality:
                        cell.infect()
        else:
            pass
        
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return "<{}, {}, {}, {}>".format(self.x, self.y, self.state, self.count)
        
class Map(object):
    
    def __init__(self):
        self.height = 150
        self.width = 150           
        self.cells = {}

    def add_cell(self, cell):
        #takes cell object and inserts it into the cells dictionary
        self.cells[(cell.x,cell.y)] = cell
        
    def display(self):
        #turn the data in the map into a suitable format
        image = [[(0.0,0.0,0.0) for x in range (150)] for y in range(150)]        
        for x,y in self.cells:
            if self.cells[(x,y)].state == "S":
                image[x][y] = (0.0,1.0,0.0) #green
            if self.cells[(x,y)] == "I":
                image[x][y] = (1.0, 0.0, 0.0) #red
            if self.cells[(x,y)].state == "R":
                image[x][y] = (0.5, 0.5, 0.5) #gray
        #call matplotlib to display it in the iPython console
        plt.imshow(image)
        pass
    
    def adjacent_cells(self, x,y):
        cell_list = []
        try:
            #north
            if y+1 <= 150:
                cell_list.append(m.cells[(x, y+1)])
            #south    
            if y-1 >= 0:
                cell_list.append(m.cells[(x, y-1)])
            #west    
            if x-1 >= 0:
                cell_list.append(m.cells[(x-1, y)])
            #east    
            if x+1 <= 150:
                cell_list.append(m.cells[(x+1, y)])
        #pay attention to the boundary fo the map
        #there cannot be cells outside of the map area
        except KeyError:
            pass
        
        return cell_list
    
    def time_step(self):
        #call the process method on each of the cells
        for x,y in self.cells:
            self.cells[(x,y)].process(self.adjacent_cells(x,y))
        #call display to display the new state of the map
        self.display()
            

            
def read_map(filename):   
    m = Map()
    #reads in x,y coordinates from a file
    f = open(filename, 'r')
    for line in f:
        line = line.strip()
        fields = line.split(",")        
        x = int(fields[0].strip())
        y = int(fields[1].strip())
        #create a new cell instance for each coordinate pair
        m.add_cell(Cell(x,y))
     #return a map instance containing all the cells   
    return m
