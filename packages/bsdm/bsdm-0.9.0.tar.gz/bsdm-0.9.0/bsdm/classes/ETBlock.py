from svgwrite import cm, mm, px  

import utils.config as config

from utils.logger import LOGGER

from classes.Drawing import Drawing
from classes.ETName import ETName
from classes.ETAttr import ETAttr

class ETBlock(object): 
        
    def __init__(self, x, y, name):
        
        self.__title = None
        self.__attrs = []
        self.__anchorsUp = []
        self.__anchorsRight = []
        self.__anchorsDown = []
        self.__anchorsLeft = []    
            
        self.__group = None
        self.update(x, y, name)
        

        
    def update(self, x=None, y=None, name=None):
        if(x is not None):
            self.__x = x
        if(y is not None):
            self.__y = y
        if(name is not None):
            self.__name = name
    
    def translate(self, tx, ty):
        self.__group.translate(tx, ty)    

    
            
    def build(self):
        _yOffset = 0
        _maxWidth = 0
        self.__height = 2 * config.MARGIN  # 10 px default margin  
        self.__width  = 2 * config.MARGIN
        
        self.__group = Drawing.DWG.g(   id=self.__name, 
                                        stroke='green',
                                        stroke_width=1*px,
                                        fill='white'       )
        
        if(self.__title is not None):
            self.__title.update(self.__x, self.__y + _yOffset)
            self.__title.build()
            _yOffset +=  self.__title.getHeight()
            _maxWidth = max(_maxWidth, self.__title.getWidth())
        
        for attr in self.__attrs:
            attr.update(self.__x, self.__y + _yOffset)
            attr.build()
            _yOffset += attr.getHeight()
            _maxWidth = max(_maxWidth, attr.getWidth())
        
        self.__height += _yOffset
        self.__width += _maxWidth   
        
        self.__block = Drawing.DWG.rect(insert=(self.__x * px, self.__y * px), 
                                        size=(self.__width * px, self.__height * px),
                                        rx = config.ROUNDING * px,
                                        ry = config.ROUNDING * px                      )
        self.__block['class'] = 'eteven'


    def draw(self):

        Drawing.DWG.add(self.__group)
        self.__group.add(self.__block)
        
        if(self.__title is not None):
            self.__title.add(self.__group)
        
        for attr in self.__attrs:
            attr.add(self.__group)

    def getX(self):
        return self.__x
    
    def getY(self):
        return self.__y
            
    def getWidth(self):
        return self.__width
    
    def getHeight(self):
        return self.__height    

    def setTitle(self, title):
        self.__title = ETName(0, 0, title)
        
    def addAttr(self, attrname, id=True, mandatory=False, deprecated=False):
        self.__attrs.append(ETAttr(0,0, attrname, id, mandatory, deprecated))