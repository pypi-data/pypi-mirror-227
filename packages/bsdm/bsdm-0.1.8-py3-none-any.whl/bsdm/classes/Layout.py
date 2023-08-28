
import random
import math

from utils.logger import LOGGER

# mass
alpha = 1.0
beta = .0001
k = 1.0
d = 0.1

#damping
eta = .99
delta_t = .01

infinity = 1000000.0



class Point(object):

    def __init__(self, x=0.0, y=0.0):
        self._x = x
        self._y = y
    
    def __add__(self, point):
        return(Point(self.getX() + point.getX(), self.getY() + point.getY()))   
    
    def __sub__(self, point):
        return(Point(self.getX() - point.getX(), self.getY() - point.getY()))       
    
    def __mul__(self, scalar):
        return(Point(self.getX() * scalar, self.getY() * scalar))     
        
    def __str__(self):
        return '('+str(self._x)+', '+str(self._y)+')'
        
    def set(self, x, y):
        self._x = x
        self._y = y   

    def getX(self):
        return self._x

    def getY(self):
        return self._y
    
    def translate(self, vector):
        self._x += vector.getX()
        self._y += vector.getY()

    def dot(self, scalar):
        self._x *= scalar
        self._y *= scalar
        
    def scale(self, vector):
        self._x *= vector.getX()
        self._y *= vector.getY()
        
    def norm(self):
        return math.sqrt(self._x * self._x + self._y * self._y)
        
        
                
Vector = Point 
    
    
class Vertice(Point):
    
    def __init__(self, name, x=0.0, y=0.0):
        self.__name = name
        super().__init__(x, y)
    
    def __str__(self):
        return 'V [ '+self.__name+':'+ super().__str__() +']'
    
        # DEBUG    
    def printDEBUG(self):
        print(self.__name+";"+str(self._x)+";"+str(self._y))
        
        
    def getName(self):
        return self.__name
    
    
class Edge(object):
    
    __SEPARATOR = '@'
    
    def __init__(self, vertice1, vertice2, intensity=1):    
        self.__vertice1 = vertice1
        self.__vertice2 = vertice2
        self.__intensity = intensity
        
    def getIntensity(self):
        return(self.__intensity)
    
    def getIdentifiers(self):
        return  self.__vertice1.getName() + Edge.__SEPARATOR + self.__vertice2.getName(), \
                self.__vertice2.getName() + Edge.__SEPARATOR + self.__vertice1.getName()
    
    @classmethod        
    def genIdentifiers(cls, vertice1, vertice2):
        return vertice1.getName()+Edge.__SEPARATOR+vertice2.getName(), vertice2.getName()+Edge.__SEPARATOR+vertice1.getName()


class Graph(object):
    
    __edges = {}     # arrêtes
    __vertices = {}  # noeuds
    
    @classmethod
    def getVerticesNumber(cls):
        return len(cls.__vertices)
    
    @classmethod
    def addEdge(cls, edge):
        identifier1, identifier2 = edge.getIdentifiers()
        
        if(identifier1 in cls.__edges or identifier2 in cls.__edges):
            LOGGER.warning('Trying to add an already existing edge.')
        
        cls.__edges[identifier1] = edge
        cls.__edges[identifier2] = edge

    @classmethod
    def addVertice(cls, vertice):
        if(vertice.getName() in cls.__vertices):
            LOGGER.warning('Trying to add a vertice with an already used name.')
        else:
            cls.__vertices[vertice.getName()] = vertice

    @classmethod
    def updateVertices(cls, vertices):
        cls.__vertices = vertices

    @classmethod
    def reset(cls):
        cls.__edges = {}  
        cls.__vertices = []        

    @classmethod  
    def print(cls):
        for vertice in cls.__vertices:
            print(cls.__vertices[vertice])
    
    @classmethod        
    def getVertices(cls):
        return cls.__vertices
    
    @classmethod        
    def getVertice(cls, name):
        if name in cls.__vertices:
            return cls.__vertices[name]    
        return None
        
    @classmethod
    def edgeExists(cls, vertice1, vertice2):
        _id1, _id2 = Edge.genIdentifiers(vertice1, vertice2)
        return _id1 in cls.__edges or _id2 in cls.__edges
    
    @classmethod
    def getEdge(cls, vertice1, vertice2):
        _id1, _id2 = Edge.genIdentifiers(vertice1, vertice2)  
        if _id1 in cls.__edges :
            return(cls.__edges[_id1])
        if _id2 in cls.__edges :
            return(cls.__edges[_id2])
        return None

    @classmethod
    def printDEBUG(cls):
        for vertice in cls.__vertices:
            cls.__vertices[vertice].printDEBUG()

class Layout(object):

    ## Spring constants and variables
    # mass
    __springAlpha  = 1.0
    __springBeta   = 0.0001
    __springK      = 1.0
    __springD      = 0.1

    #damping
    __springEta    = 0.99
    __springDeltaT = 0.01
    
    __springStep   = 0

    
    @classmethod        
    def initSpringAlgorithm(cls, step=500, limit=0):
        cls.__vertices = Graph.getVertices()
    
        cls.__springSpeeds = {}
        cls.__springStep   = step
        cls.__springLimit  = limit
    
        for vertice in cls.__vertices:
            vertice = cls.__vertices[vertice]
            vertice.set(random.random(), random.random())               # set random position
            cls.__springSpeeds[vertice.getName()] = Vector(0.0, 0.0)    # set initial speed
            
        
    @classmethod 
    def runSpringAlgorithm(cls):
        while (cls.__springStep > 0):
            cls.__springStep -= 1
            kineticEnergy = cls.__springLoop() 
            Graph.updateVertices(cls.__vertices)  
            if(kineticEnergy < cls.__springLimit):
                return         
            
    @classmethod
    def normalize(cls, grid=0):
        _xMin = infinity
        _yMin = infinity
        _xMax = 0
        _yMax = 0

        for vertice in cls.__vertices:
            vertice = cls.__vertices[vertice]
            
            _xMin = min(_xMin, vertice.getX())  
            _yMin = min(_yMin, vertice.getY())
            _xMax = max(_xMax, vertice.getX())  
            _yMax = max(_yMax, vertice.getY())            
        
        _scaleX = 1 / (_xMax - _xMin)
        _scaleY = 1 / (_yMax - _yMin)
            
        for vertice in cls.__vertices:
            vertice = cls.__vertices[vertice]
            
            vertice.translate( Vector(- _xMin, - _yMin) )
            vertice.scale( Vector(_scaleX, _scaleY) )
            
            # alignement sur la grille
            if(grid > 0) :

                _x = (vertice.getX() % grid)
                if(_x < grid / 2):
                    _x = vertice.getX() - _x
                else:
                    _x = vertice.getX() - _x + grid    
                _x = round(_x, 5)
            
                _y = (vertice.getY() % grid)
                if(_y < grid / 2):
                    _y = vertice.getY() - _y
                else:
                    _y = vertice.getY() - _y + grid    
                _y = round(_y, 5)
            
                vertice.set(x=_x, y=_y)
            
            
    
    @classmethod
    def __springRepulsiveForce(cls, vertice1, vertice2):  # Coulomb law 
    
        if(vertice1 == vertice2):
            return Vector(0.0, 0.0)
        delta = vertice2 - vertice1

        distance = delta.norm()  

        if(distance != 0.0):
            const = cls.__springBeta / (distance**3)
        else:
            const = cls.__springBeta * infinity

        return delta * (- const)


    @classmethod
    def __springAttractiveForce(cls, vertice1, vertice2, intensity): #Hooke law

        if(vertice1 == vertice2):
            return Vector(0.0, 0.0)

        delta = vertice2 - vertice1
        
        distance = delta.norm()

        #const = cls.__springK * (distance - cls.__springD) / distance                 # original
        
        #const = distance - (cls.__springD / intensity)      # new step 1
        #const /= distance                                   #     step 2
        #const *= cls.__springK                              #     step 3

        const = (distance - (cls.__springD / (intensity**intensity))) / distance * cls.__springK # new



        return delta * const
    
    
    @classmethod     
    def __springLoop(cls):
        
        kineticEnergy = Vector(0.0, 0.0) # initialize force
        
        for vertice1 in cls.__vertices:
            vertice1 = cls.__vertices[vertice1]
            
            force = Vector(0.0, 0.0) # initialize force
        
            for vertice2 in cls.__vertices:
                vertice2 = cls.__vertices[vertice2]

                # compute force
                _edge = Graph.getEdge(vertice1, vertice2)
                if(_edge is not None) :
                    intensity = _edge.getIntensity() 
                    force += cls.__springAttractiveForce(vertice1, vertice2, intensity)
                force += cls.__springRepulsiveForce(vertice1, vertice2)           

            # update speed
            _speedX = cls.__springSpeeds[vertice1.getName()].getX() + cls.__springAlpha * force.getX() * cls.__springDeltaT 
            _speedY = cls.__springSpeeds[vertice1.getName()].getY() + cls.__springAlpha * force.getY() * cls.__springDeltaT 

            cls.__springSpeeds[vertice1.getName()] = Vector(_speedX, _speedY) * cls.__springEta

            tmpVertice = cls.__vertices[vertice1.getName()] + (cls.__springSpeeds[vertice1.getName()] * cls.__springDeltaT) # to delete

        # update position
        for vertice in cls.__vertices:
            tmpVertice = cls.__vertices[vertice] + (cls.__springSpeeds[vertice] * cls.__springDeltaT)
            cls.__vertices[vertice].set(tmpVertice.getX(), tmpVertice.getY())
            
        #compute kinetic energy
            _kinEX = kineticEnergy.getX() + cls.__springAlpha * (cls.__springSpeeds[vertice].getX() ** 2) 
            _kinEY = kineticEnergy.getY() + cls.__springAlpha * (cls.__springSpeeds[vertice].getY() ** 2)
            kineticEnergy = Vector(_kinEX, _kinEY)
            
        kineticEnergy = kineticEnergy.norm()
        
        return kineticEnergy


def layout(jsonDescription):
    
    _jsonDescription = jsonDescription
    
    # Build graph
    
    vA = Vertice('A')
    vB = Vertice('B')  
    vC = Vertice('C')
    vD = Vertice('D') 
    vE = Vertice('E')   
    vF = Vertice('F')  
    
    eAB = Edge(vA, vB)
    eBC = Edge(vB, vC)
    eCA = Edge(vC, vA)
    eCD = Edge(vC, vD, 10)
    eAE = Edge(vA, vE)
    eBE = Edge(vB, vE)
    eCF = Edge(vC, vF, 10)
    eDF = Edge(vD, vF, 100)
    
    Graph.addVertice(vA)
    Graph.addVertice(vB)
    Graph.addVertice(vC)
    Graph.addVertice(vD)
    Graph.addVertice(vE)
    Graph.addVertice(vF)
    
    
    Graph.addEdge(eAB)
    Graph.addEdge(eBC)
    Graph.addEdge(eCA)
    Graph.addEdge(eCD)
    Graph.addEdge(eAE)
    Graph.addEdge(eBE)
    Graph.addEdge(eCF)
    Graph.addEdge(eDF)    

    Layout.initSpringAlgorithm(step=1000000, limit=0.00000000000000000001)
    Layout.runSpringAlgorithm()
    Layout.normalize(grid=1/10)
    
    return Graph