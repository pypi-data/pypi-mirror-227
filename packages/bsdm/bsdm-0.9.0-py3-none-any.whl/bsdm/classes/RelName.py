from svgwrite import cm, mm, px  

import utils.config as config

from utils.logger import LOGGER

from classes.Text import Text
from classes.RelAnchor import RelAnchor

class RelName(Text):

    __MARGIN = 10

    def __init__(self, x=0, y=0, text='', orientation = 'UO'):
        
        self._styleClass = 'relname'

        super().__init__(0, 0, text, styleClass = self._styleClass, margin=0)
        
        _x, _y = self.__guessBestPos(x, y, orientation)

        self.update(x=_x, y=_y)        
        #self.update(text=text+ ' '+orientation)
        
        
    def __guessBestPos(self, x, y, orientation):
        
        _x = x
        _y = y
        
        match orientation:
            case 'UO':
                _x = x - (self.getWidth() + RelName.__MARGIN)
                _y = y - (self.getHeight() + RelName.__MARGIN)
            case 'UE':
                _x = x + RelName.__MARGIN
                _y = y - (self.getHeight() + RelName.__MARGIN)
            case 'RN':
                _x = x + RelName.__MARGIN
                _y = y + RelName.__MARGIN
            case 'RS':
                _x = x + RelName.__MARGIN
                _y = y + RelName.__MARGIN           
            case 'DO':
                _x = x - (self.getWidth() + RelName.__MARGIN)
                _y = y + RelName.__MARGIN 
            case 'DE':
                _x = x + RelName.__MARGIN
                _y = y + RelName.__MARGIN
            case 'LN':
                _x = x - (self.getWidth() + RelName.__MARGIN)
                _y = y + RelName.__MARGIN  
            case 'LS':
                _x = x - (self.getWidth() + RelName.__MARGIN)  
                _y = y - (self.getHeight() + RelName.__MARGIN)        
            case _ :
                pass
        
        return _x, _y 

