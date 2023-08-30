
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
        
    def __eq__(self, other):
        return self.getX() == other.getX() and self.getX() == other.getX()    
        
    def __ge__(self, other):
        return self.norm() >= other.norm()    
        
    def __lt__(self, other):
        return self.norm() < other.norm()
    
    def __le__(self, other):
        return self.norm() <= other.norm()
    
    def __gt__(self, other):
        return self.norm() > other.norm()
    
    def __ne__(self, other):
        return self.getX() != other.getX() or self.getX() != other.getX()       
        
        
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
    
    _edges = {}     # arrêtes
    _vertices = {}  # noeuds
    
    @classmethod
    def getVerticesNumber(cls):
        return len(cls._vertices)
    
    @classmethod
    def addEdge(cls, edge):
        identifier1, identifier2 = edge.getIdentifiers()
        
        if(identifier1 in cls._edges or identifier2 in cls._edges):
            LOGGER.warning('Trying to add an already existing edge.')
        
        cls._edges[identifier1] = edge
        cls._edges[identifier2] = edge

    @classmethod
    def addVertice(cls, vertice):
        if(vertice.getName() in cls._vertices):
            LOGGER.warning('Trying to add a vertice with an already used name.')
        else:
            cls._vertices[vertice.getName()] = vertice

    @classmethod
    def updateVertices(cls, vertices):
        cls._vertices = vertices

    @classmethod
    def reset(cls):
        cls._edges = {}  
        cls._vertices = []        

    @classmethod  
    def print(cls):
        for vertice in cls._vertices:
            print(cls._vertices[vertice])
    
    @classmethod        
    def getVertices(cls):
        return cls._vertices
    
    @classmethod        
    def getVertice(cls, name):
        if name in cls._vertices:
            return cls._vertices[name]    
        return None
        
    @classmethod
    def edgeExists(cls, vertice1, vertice2):
        _id1, _id2 = Edge.genIdentifiers(vertice1, vertice2)
        return _id1 in cls._edges or _id2 in cls._edges
    
    @classmethod
    def getEdge(cls, vertice1, vertice2):
        _id1, _id2 = Edge.genIdentifiers(vertice1, vertice2)  
        if _id1 in cls._edges :
            return(cls._edges[_id1])
        if _id2 in cls._edges :
            return(cls._edges[_id2])
        return None

    @classmethod
    def printDEBUG(cls):
        print('DEBUG ('+str(cls)+') :')
        for vertice in cls._vertices:
            cls._vertices[vertice].printDEBUG()

class Layout(Graph):

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
    
        cls.__springSpeeds = {}
        cls.__springStep   = step
        cls.__springLimit  = limit
    
        for vertice in cls._vertices:
            vertice = cls._vertices[vertice]
            vertice.set(random.random(), random.random())               # set random position
            cls.__springSpeeds[vertice.getName()] = Vector(0.0, 0.0)    # set initial speed
            
        
    @classmethod 
    def runSpringAlgorithm(cls):
        while (cls.__springStep > 0):
            cls.__springStep -= 1
            kineticEnergy = cls.__springLoop() 
            cls.updateVertices(cls._vertices)  
            if(kineticEnergy < cls.__springLimit):
                return         
            
    @classmethod
    def normalize(cls, grid=0):
        _xMin = infinity
        _yMin = infinity
        _xMax = 0
        _yMax = 0

        for vertice in cls._vertices:
            vertice = cls._vertices[vertice]
            
            _xMin = min(_xMin, vertice.getX())  
            _yMin = min(_yMin, vertice.getY())
            _xMax = max(_xMax, vertice.getX())  
            _yMax = max(_yMax, vertice.getY())            
        
        _scaleX = 1 / (_xMax - _xMin)
        _scaleY = 1 / (_yMax - _yMin)
            
        for vertice in cls._vertices:
            vertice = cls._vertices[vertice]
            
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
        
        for vertice1 in cls._vertices:
            vertice1 = cls._vertices[vertice1]
            
            force = Vector(0.0, 0.0) # initialize force
        
            for vertice2 in cls._vertices:
                vertice2 = cls._vertices[vertice2]

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

            tmpVertice = cls._vertices[vertice1.getName()] + (cls.__springSpeeds[vertice1.getName()] * cls.__springDeltaT) # to delete

        # update position
        for vertice in cls._vertices:
            tmpVertice = cls._vertices[vertice] + (cls.__springSpeeds[vertice] * cls.__springDeltaT)
            cls._vertices[vertice].set(tmpVertice.getX(), tmpVertice.getY())
            
        #compute kinetic energy
            _kinEX = kineticEnergy.getX() + cls.__springAlpha * (cls.__springSpeeds[vertice].getX() ** 2) 
            _kinEY = kineticEnergy.getY() + cls.__springAlpha * (cls.__springSpeeds[vertice].getY() ** 2)
            kineticEnergy = Vector(_kinEX, _kinEY)
            
        kineticEnergy = kineticEnergy.norm()
        
        return kineticEnergy

    @classmethod
    def spring(cls, dictDescription, grid=1/10):
        
        _dictDescription = dictDescription
        _grid=grid
        
        for entity in _dictDescription['entities']:
            cls.addVertice(Vertice(entity['name']))
        
        for relation in _dictDescription['relations']:
            vertice1 = cls.getVertice(relation['et1'])
            vertice2 = cls.getVertice(relation['et2'])
            
            intensity = 1
            if 'intensity' in relation:
                intensity = int(relation['intensity'])
                
            cls.addEdge(Edge(vertice1, vertice2, intensity))
        

        cls.initSpringAlgorithm(step=1000000, limit=0.0000000000000000000001)
        cls.runSpringAlgorithm()   
        
        cls.normalize(_grid)
        
        
        
    @classmethod
    def scale(cls, scaleFactor):
        for vertice in cls._vertices:
            vertice = cls._vertices[vertice]
            vertice.dot(scaleFactor)
        
        
    @classmethod
    def cleverScale(cls, blocks, scaleFactor): 
        
        cls.scale(scaleFactor)
        
        cls._vertices = dict(sorted(cls._vertices.items(), key=lambda x:x[1]))        
        tmpVertices = dict(cls._vertices)

        for vertice1 in cls._vertices:
            tmpVertices.pop(vertice1)
            
            vertice1 = cls._vertices[vertice1]
            
            _block = blocks[vertice1.getName()]
            
            _blockWidth = _block.getWidth()
            _blockHeight = _block.getHeight()            
            _boundaryX = _block.getX() + _blockWidth
            _boundaryY = _block.getY() + _blockHeight         

            for vertice2 in tmpVertices:
                
                vertice2 = cls._vertices[vertice2]

                _oldX = vertice2.getX()
                _oldY = vertice2.getY()
                _newX = _oldX
                _newY = _oldY
                
                if _oldY <= _boundaryY:
                    _newX = _oldX + _blockWidth
                    
                if _oldX <= _boundaryX:
                    _newY = _oldY + _blockHeight                    
                    
                vertice2.set(_newX, _newY)