from svgwrite import cm, mm, px  

import utils.config as config

from utils.logger import LOGGER

from classes.Drawing import Drawing


class Anchor(object):
    
    __PADDING = 25
    
    def __init__(self, x1, y1, x2, y2, width, height):
        self.update(x1, y1, x2, y2, width, height)
        
    def update(self, x1=None, y1=None, x2=None, y2=None, width=None, height=None):
        if(x1 is not None):
            self.__x1 = x1
        if(y1 is not None):
            self.__y1 = y1
        if(x2 is not None):
            self.__x2 = x2
        if(y2 is not None):
            self.__y2 = y2
        if(width is not None):
            self.__width = width
        if(height is not None):
            self.__height = height

    def getX(self):
        return self.__xEnd

    def getY(self):
        return self.__yEnd

    def build(self):
        
        choice = 100000
        
        _a = (self.__y2 - self.__y1)/(self.__x2 - self.__x1)
        _c = self.__y1 - _a * self.__x1

        _xA = self.__x1 + (1/2 * self.__width)
        _yA = _a * _xA + _c
        
        test = (_xA - self.__x1) * (self.__x2 - self.__x1) + (_yA - self.__y1) * (self.__y2 - self.__y1)
        if(test > 0 and test < choice) :
            choice = test
            self.__xStart = _xA     
            self.__xEnd = _xA + Anchor.__PADDING      
            self.__yStart = _yA    
            self.__yEnd = _yA  
            
        _xA = self.__x1 - (1/2 * self.__width)
        _yA = _a * _xA + _c
        
        test = (_xA - self.__x1) * (self.__x2 - self.__x1) + (_yA - self.__y1) * (self.__y2 - self.__y1)
        if(test > 0 and test < choice) :
            choice = test
            self.__xStart = _xA     
            self.__xEnd = _xA - Anchor.__PADDING      
            self.__yStart = _yA    
            self.__yEnd = _yA    
    
        _yA = self.__y1 + (1/2 * self.__height)
        _xA = (_yA - _c) / _a 
        
        test = (_xA - self.__x1) * (self.__x2 - self.__x1) + (_yA - self.__y1) * (self.__y2 - self.__y1)
        if(test > 0 and test < choice) :
            choice = test
            self.__xStart = _xA     
            self.__xEnd = _xA       
            self.__yEnd = _yA + Anchor.__PADDING   
            self.__yStart = _yA 
        
        _yA = self.__y1 - (1/2 * self.__height)
        _xA = (_yA - _c) / _a
        
        test = (_xA - self.__x1) * (self.__x2 - self.__x1) + (_yA - self.__y1) * (self.__y2 - self.__y1)
        if(test > 0 and test < choice) :
            choice = test
            self.__xStart = _xA     
            self.__xEnd = _xA       
            self.__yEnd = _yA - Anchor.__PADDING   
            self.__yStart = _yA         

        self.__circleStart = Drawing.DWG.circle(center=(self.__xStart, self.__yStart), r=5)        
        self.__circleEnd = Drawing.DWG.circle(center=(self.__xEnd, self.__yEnd), r=5)


    def draw(self):
        Drawing.DWG.add(self.__circleEnd)
        Drawing.DWG.add(self.__circleStart)

class Relation(object): 
        
    def __init__(self, x1, y1, width1, height1, x2, y2, width2, height2):
    
        self.update(x1, y1, width1, height1, x2, y2, width2, height2)
        
    
    def update(self, x1=None, y1=None, width1=None, height1=None, x2=None, y2=None, width2=None, height2=None):
        if(x1 is not None):
            self.__x1 = x1
        if(y1 is not None):
            self.__y1 = y1
        if(width1 is not None):
            self.__width1 = width1
        if(height1 is not None):
            self.__height1 = height1    
        
        if(x2 is not None):
            self.__x2 = x2
        if(y2 is not None):
            self.__y2 = y2            
        if(width2 is not None):
            self.__width2 = width2
        if(height1 is not None):
            self.__height2 = height2
            
        self.__xMid = (self.__x1 + self.__x2) /2
        self.__yMid = (self.__y1 + self.__y2) /2
        
        self.__anchor1=Anchor(self.__x1, self.__y1, self.__xMid, self.__yMid, self.__width1, self.__height1)
        self.__anchor2=Anchor(self.__x2, self.__y2, self.__xMid, self.__yMid, self.__width2, self.__height2)
    
            
    def build(self):
        
        self.__anchor1.build()
        self.__anchor2.build()
        
        self.__xMid = (self.__anchor1.getX() + self.__anchor2.getX()) /2
        self.__yMid = (self.__anchor1.getY() + self.__anchor2.getY()) /2
        
        self.__line1 = Drawing.DWG.line((self.__anchor1.getX(),self.__anchor1.getY()) , (self.__xMid,self.__yMid)) 
        self.__line2 = Drawing.DWG.line((self.__xMid,self.__yMid), (self.__anchor2.getX(),self.__anchor2.getY()))     
    
        self.__line1['class'] = 'mandatoryrelationshipline'
        self.__line2['class'] = 'mandatoryrelationshipline'
        

    def draw(self):

        Drawing.DWG.add(self.__line1)        
        Drawing.DWG.add(self.__line2)
        
        self.__anchor1.draw()
        self.__anchor2.draw()


