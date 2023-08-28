# bsdm.py

import argparse

from svgwrite import cm, mm, px  

from pathlib import Path

import json

import utils.config as config

from utils.logger import LOGGER
from utils.StyleSheet import StyleSheet

from classes.Drawing import Drawing
from classes.ETBlock import ETBlock
from classes.ETAnchor import ETAnchorPosition

from classes.Layout import layout




def checkArgs():
    """
Checks and saves arguments passed when calling the program.

Returns the list of arguments if successful.
Otherwise, terminates the program.

Arguments: none
    """    
    
    parser = argparse.ArgumentParser(
        prog='BSDM',
        description='Beautiful SVG Data Model',
        epilog='Generate SVG beautiful diagram with CSS from Oracle Data Modeler.')

    parser.add_argument('-c','--css_file', required=False, help='css filename')
    parser.add_argument('data_model', help='Data Model directory')
    parser.add_argument('-o', '--output_svg_file', help='SVG output filename') 

    args = parser.parse_args()
    
    return args
    
    
def setOutputSVGPath(output_svg_file_arg):
    """
Builds, if necessary, the path for the program's output SVG file.

Returns a clean path corresponding to the one passed as argument.

Arguments:
output_svg_file_arg: a string designating the output SVG file.    
    """
    
    if(output_svg_file_arg):
        _svg_file_path = output_svg_file_arg
    else :
        _svg_file_path = "./data_model.svg"
    _svg_file_path = Path(_svg_file_path).resolve()
    _svg_file_path.parent.mkdir(parents=True, exist_ok=True)

    return _svg_file_path


def getInputCSS(input_css_file):
    """
Builds, if necessary, the path for the SVG CSS style file.

Returns a string containing the CSS style ot None if no CSS file passed in argument

Arguments:
input_css_file: a string designating the input CSS file.    
    """
    
    if(input_css_file):
        _css_file_path = input_css_file
    else :
        return None
    
    _css_file_path = Path(_css_file_path).resolve()

    if(_css_file_path.exists() and _css_file_path.is_file()):
        with open(str(_css_file_path), "r") as _css_file :
            return _css_file.read() 

    LOGGER.warning('Problem with CSS file. Skipping it')

    return None

def buildFromJSONDescription(jsonDescription):
    
    _jsonDescription = jsonDescription
    
    _graph = layout(_jsonDescription)
    _graph.printDEBUG()
    
    return _jsonDescription

def bsdm():

    args = checkArgs()
    
    LOGGER.info('BSDM is not what you think!')
    LOGGER.info(args.css_file + ", " +  args.output_svg_file + ", " +  args.data_model)    

    outputSVGPath = setOutputSVGPath(args.output_svg_file)
    cssStyleSheet = getInputCSS(args.css_file)  
    
    Drawing.create(outputSVGPath, cssStyleSheet)

    jsonDescription =  \
    {
        'entities' : \
        [
            {'name' : 'A'},
            {'name' : 'B'},
            {'name' : 'C'},
        ]
    }
    
    
    
    """
    
    _graph = layout()
    vertices = _graph.getVertices()
    
    _graph.printDEBUG()
    
    for vertice in vertices:
        vertice = vertices[vertice]
        vertice.dot(800) 
    
        _block = ETBlock(50, 50, 'first_block')
        _block.setTitle('TITLE '+str(vertice.getName()))
        _block.addAttr('Kouroukoukou', id=True, mandatory=False, deprecated=False)
        _block.addAttr('attttribute attrt  attr', id=True, mandatory=False, deprecated=True)
        
        _block.update(x=vertice.getX(), y=vertice.getY())
    
    
        #_block.addAnchor(ETAnchorPosition.UP)


        _block.build()
    
    #_block.translate(400, 400)    
    
    #Drawing.reset()
    
    Drawing.write()
    
    """


def main():
    bsdm()

if __name__ == "__main__":
    main()
    
    