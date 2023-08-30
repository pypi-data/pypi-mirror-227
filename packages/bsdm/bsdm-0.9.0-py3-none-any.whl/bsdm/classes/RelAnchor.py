from svgwrite import cm, mm, px  

import utils.config as config

from utils.logger import LOGGER

from classes.Drawing import Drawing


class RelAnchor(object):
    
    PADDING = 25
    __MARGIN = config.MARGIN
    
    def __init__(self, x1, y1, x2, y2, width, height, card='one', mandatory = True, hvLines=False):
        self.update(x1, y1, x2, y2, width, height, card, mandatory, hvLines)
        
    def update(self, x1=None, y1=None, x2=None, y2=None, width=None, height=None, card='one', mandatory = True, hvLines=False):
        if(x1 is not None):
            self.__x1 = x1
        if(y1 is not None):
            self.__y1 = y1
        if(x2 is not None):
            self.__x2 = x2
        if(y2 is not None):
            self.__y2 = y2
        if(width is not None):
            self.__width = width - (2 * RelAnchor.__MARGIN)
        if(height is not None):
            self.__height = height - (2 * RelAnchor.__MARGIN)
        self.__card = card
        self.__mandatory = mandatory
        self.__hvLines = hvLines

    def getXEnd(self):
        return self.__xEnd

    def getYEnd(self):
        return self.__yEnd
    
    def getXStart(self):
        return self.__xStart

    def getYStart(self):
        return self.__yStart
    
    def getOrientation(self):
        return self.__orientation

    def build(self):
        
        _infinity = 100000
        
        try:
            _a = (self.__y2 - self.__y1)/(self.__x2 - self.__x1)
        except ZeroDivisionError as e :
            print('PT1 : ('+str(self.__x1)+' , '+ str(self.__y1)+')') 
            print('PT2 : ('+str(self.__x2)+' , '+ str(self.__y2)+')') 
            print(e)
            _a = _infinity
        
        _c = self.__y1 - _a * self.__x1
        
        
        _xA = self.__x1 + (1/2 * self.__width)
        _yA = _a * _xA + _c
        
        test = (_xA - self.__x1) * (self.__x2 - self.__x1) + (_yA - self.__y1) * (self.__y2 - self.__y1)
        if(test > 0 and test < _infinity) :
            _infinity = test
            self.__xStart = _xA + RelAnchor.__MARGIN   
            self.__xEnd = _xA + (RelAnchor.PADDING + RelAnchor.__MARGIN)    
            if(self.__hvLines):
                self.__xEnd = self.__x2     
            self.__yStart = _yA    
            self.__yEnd = _yA  
            self.__orientation = 'R'
            
        _xA = self.__x1 - (1/2 * self.__width)
        _yA = _a * _xA + _c
        
        test = (_xA - self.__x1) * (self.__x2 - self.__x1) + (_yA - self.__y1) * (self.__y2 - self.__y1)
        if(test > 0 and test < _infinity) :
            _infinity = test
            self.__xStart = _xA - RelAnchor.__MARGIN    
            self.__xEnd = _xA - (RelAnchor.PADDING + RelAnchor.__MARGIN)
            if(self.__hvLines):
                self.__xEnd = self.__x2       
            self.__yStart = _yA    
            self.__yEnd = _yA    
            self.__orientation = 'L'
    
        _yA = self.__y1 + (1/2 * self.__height)
        try:
            _xA = (_yA - _c) / _a 
        except ZeroDivisionError as e :
            print('PT1 : ('+str(self.__x1)+' , '+ str(self.__y1)+')') 
            print('PT2 : ('+str(self.__x2)+' , '+ str(self.__y2)+')') 
            print(e)
            _xA = (_yA - _c) * _infinity
        
        test = (_xA - self.__x1) * (self.__x2 - self.__x1) + (_yA - self.__y1) * (self.__y2 - self.__y1)
        if(test > 0 and test < _infinity) :
            _infinity = test
            self.__xStart = _xA     
            self.__xEnd = _xA    
            self.__yEnd = _yA + (RelAnchor.PADDING + RelAnchor.__MARGIN)
            if(self.__hvLines):
                self.__yEnd = self.__y2 
            self.__yStart = _yA + RelAnchor.__MARGIN
            self.__orientation = 'D'
        
        _yA = self.__y1 - (1/2 * self.__height)
        try:
            _xA = (_yA - _c) / _a
        except ZeroDivisionError as e :
            print('PT1 : ('+str(self.__x1)+' , '+ str(self.__y1)+')') 
            print('PT2 : ('+str(self.__x2)+' , '+ str(self.__y2)+')') 
            print(e)
            _xA = (_yA - _c) * _infinity
        
        test = (_xA - self.__x1) * (self.__x2 - self.__x1) + (_yA - self.__y1) * (self.__y2 - self.__y1)
        if(test > 0 and test < _infinity) :
            _infinity = test
            self.__xStart = _xA     
            self.__xEnd = _xA       
            self.__yEnd = _yA - (RelAnchor.PADDING + RelAnchor.__MARGIN)   
            if(self.__hvLines):
                self.__yEnd = self.__y2 
            self.__yStart = _yA - RelAnchor.__MARGIN   
            self.__orientation = 'U'     


        self.__line = Drawing.DWG.line((self.__xStart, self.__yStart), (self.__xEnd, self.__yEnd))
        if  self.__mandatory:
            self.__line['class'] = 'mandatoryrelationshipline' 
        else:
            self.__line['class'] = 'optionalrelationshipline'       
        

        if self.__card == 'many' :
            if(self.__xStart == self.__xEnd):
                _xcfL11 = self.__xStart - 5
                _xcfL12 = self.__xEnd
                _xcfL21 = self.__xStart + 5
                _xcfL22 = self.__xEnd
                if(self.__yStart > self.__yEnd):
                    _ycfL11 = self.__yStart
                    _ycfL12 = self.__yStart - 10
                    _ycfL21 = self.__yStart
                    _ycfL22 = self.__yStart - 10
                else:
                    _ycfL11 = self.__yStart
                    _ycfL12 = self.__yStart + 10
                    _ycfL21 = self.__yStart
                    _ycfL22 = self.__yStart + 10 
            else:
                _ycfL11 = self.__yStart - 5
                _ycfL12 = self.__yEnd
                _ycfL21 = self.__yStart + 5
                _ycfL22 = self.__yEnd
                if(self.__xStart > self.__xEnd):
                    _xcfL11 = self.__xStart
                    _xcfL12 = self.__xStart - 10
                    _xcfL21 = self.__xStart
                    _xcfL22 = self.__xStart - 10
                else:
                    _xcfL11 = self.__xStart
                    _xcfL12 = self.__xStart + 10
                    _xcfL21 = self.__xStart
                    _xcfL22 = self.__xStart + 10                 
                
            
            self.__crowfootLine1 = Drawing.DWG.line((_xcfL11, _ycfL11) , (_xcfL12, _ycfL12))
            self.__crowfootLine2 = Drawing.DWG.line((_xcfL21, _ycfL21) , (_xcfL22, _ycfL22))
            
            if  self.__mandatory:
                self.__crowfootLine1['class'] = 'mandatoryrelationshipline'             
                self.__crowfootLine2['class'] = 'mandatoryrelationshipline' 
            else:
                self.__crowfootLine1['class'] = 'optionalrelationshipline'
                self.__crowfootLine2['class'] = 'optionalrelationshipline'

        self.__circleStart = Drawing.DWG.circle(center=(self.__xStart, self.__yStart), r=5)        
        self.__circleEnd = Drawing.DWG.circle(center=(self.__xEnd, self.__yEnd), r=5)


    def draw(self):
        Drawing.DWG.add(self.__line)
        
        if self.__card == 'many' :
            Drawing.DWG.add(self.__crowfootLine1)
            Drawing.DWG.add(self.__crowfootLine2)
        
        #Drawing.DWG.add(self.__circleEnd)
        #Drawing.DWG.add(self.__circleStart)
        



