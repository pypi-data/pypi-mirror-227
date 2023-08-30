
import svgwrite
from svgwrite import cm, mm, px  

from pathlib import Path

import utils.config as config

from utils.logger import LOGGER
from utils.StyleSheet import StyleSheet


class Drawing(object):
    
    DWG = None
    
    @classmethod    
    def setOutputSVGPath(cls, outputSVGPath):
        if(outputSVGPath is not None):
            cls.__outputSVGPath = outputSVGPath
    
    @classmethod    
    def setCssStyleSheet(cls, cssStyleSheet):
        if(cssStyleSheet is not None):
            cls.__cssStyleSheet = cssStyleSheet
        
    @classmethod    
    def setSize(cls, size):
        if(size is not None):
            cls.__size = size
        else:
            cls.__size = None
        
    @classmethod
    def create(cls, outputSVGPath, size = None, cssStyleSheet = None):
        
        cls.setOutputSVGPath(outputSVGPath)
        cls.setCssStyleSheet(cssStyleSheet)
        cls.setSize(size)
        
        cls.DWG = svgwrite.Drawing(cls.__outputSVGPath, size=cls.__size, debug=True)
        if(cls.__cssStyleSheet is not None) :
            cls.DWG.embed_stylesheet(cls.__cssStyleSheet)
            StyleSheet.loadFromCSSStyleSheet(cls.__cssStyleSheet) 

    @classmethod            
    def reset(cls):
        cls.create(cls.__outputSVGPath, cls.__size, cls.__cssStyleSheet)


    @classmethod        
    def write(cls):
        cls.DWG.save(pretty=True)