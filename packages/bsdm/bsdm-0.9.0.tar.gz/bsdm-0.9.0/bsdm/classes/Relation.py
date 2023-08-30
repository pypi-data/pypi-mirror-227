from svgwrite import cm, mm, px  

import utils.config as config

from utils.logger import LOGGER

from classes.Drawing import Drawing
from classes.RelAnchor import RelAnchor
from classes.RelName import RelName

class Relation(object): 
    
    @classmethod
    def __getOrientation(cls, xet1,yet1, xet2, yet2, anchorOrientation):
        
        _orientation = anchorOrientation
        
        match _orientation:
            case 'U' | 'D':
                if(xet1 < xet2):
                    _orientation += 'E'
                else:
                    _orientation += 'O'
            case 'R' | 'L':
                if(yet1 < yet2):
                    _orientation += 'S'
                else:
                    _orientation += 'N'                    
            case _:
                _orientation = '??'
        
        return _orientation
        
    def __init__(self,  entity1, entity2, 
                        entity1Card='one', entity2Card='one', 
                        entity1Mandatory=True, entity2Mandatory=True, 
                        entity1RelName=None, entity2RelName=None,
                        hvLines=False):
    
        self.update(entity1, entity2, 
                    entity1Card, entity2Card, 
                    entity1Mandatory, entity2Mandatory, 
                    entity1RelName, entity2RelName,
                    hvLines)
        
    
    def update(self,    entity1, entity2, 
                        entity1Card='one', entity2Card='one', 
                        entity1Mandatory=True, entity2Mandatory=True, 
                        entity1RelName=None, entity2RelName=None,
                        hvLines=False):

        self._entity1 = entity1
        self.__width1 = self._entity1.getWidth()
        self.__height1 = self._entity1.getHeight()   
        self.__x1 = self._entity1.getX() + self.__width1/2
        self.__y1 = self._entity1.getY() + self.__height1/2
        self.__entity1Card = entity1Card 
        self.__entity1Mandatory = entity1Mandatory
        self.__entity1RelName = entity1RelName

        self._entity2 = entity2
        self.__width2 = self._entity2.getWidth()
        self.__height2 = self._entity2.getHeight()   
        self.__x2 = self._entity2.getX() + self.__width2/2
        self.__y2 = self._entity2.getY() + self.__height2/2
        self.__entity2Card = entity2Card 
        self.__entity2Mandatory = entity2Mandatory
        self.__entity2RelName = entity2RelName      
        
        self.__hvLines = hvLines  
            
        self.__xMid = (self.__x1 + self.__x2) /2
        self.__yMid = (self.__y1 + self.__y2) /2
        
        self.__anchor1=RelAnchor(   self.__x1, self.__y1, 
                                    self.__xMid, self.__yMid, 
                                    self.__width1, self.__height1, 
                                    self.__entity1Card, self.__entity1Mandatory,
                                    self.__hvLines)
        self.__anchor2=RelAnchor(   self.__x2, self.__y2, 
                                    self.__xMid, self.__yMid, 
                                    self.__width2, self.__height2, 
                                    self.__entity2Card, self.__entity2Mandatory,
                                    self.__hvLines)
    
            
    def build(self):
        
        self.__anchor1.build()
        self.__anchor2.build()
        
        self.__xMid = (self.__anchor1.getXEnd() + self.__anchor2.getXEnd()) /2
        self.__yMid = (self.__anchor1.getYEnd() + self.__anchor2.getYEnd()) /2
        
        self.__line1 = Drawing.DWG.line((self.__anchor1.getXEnd(),self.__anchor1.getYEnd()) , (self.__xMid,self.__yMid)) 
        if  self.__entity1Mandatory:
            self.__line1['class'] = 'mandatoryrelationshipline'
        else:
            self.__line1['class'] = 'optionalrelationshipline'
        
        self.__line2 = Drawing.DWG.line((self.__xMid,self.__yMid), (self.__anchor2.getXEnd(),self.__anchor2.getYEnd()))     
        if  self.__entity2Mandatory:
            self.__line2['class'] = 'mandatoryrelationshipline'
        else:
            self.__line2['class'] = 'optionalrelationshipline'
            
        self.__relName1 = None
        if self.__entity1RelName is not None :
            _orientation = Relation.__getOrientation(   self.__x1, self.__y1, 
                                                        self.__x2, self.__y2, 
                                                        self.__anchor1.getOrientation())   
            self.__relName1 = RelName(self.__anchor1.getXStart(), self.__anchor1.getYStart(), self.__entity1RelName, _orientation)
            self.__relName1.build()
            
        self.__relName2 = None
        if self.__entity2RelName is not None :
            _orientation = Relation.__getOrientation(   self.__x2, self.__y2, 
                                                        self.__x1, self.__y1, 
                                                        self.__anchor2.getOrientation())
            self.__relName2 = RelName(self.__anchor2.getXStart(), self.__anchor2.getYStart(), self.__entity2RelName, _orientation)
            self.__relName2.build()


    def draw(self):

        Drawing.DWG.add(self.__line1)        
        Drawing.DWG.add(self.__line2)
        
        self.__anchor1.draw()
        self.__anchor2.draw()
        
        if self.__relName1 is not None :
            self.__relName1.add(Drawing.DWG)
            
        if self.__relName2 is not None :
            self.__relName2.add(Drawing.DWG)


