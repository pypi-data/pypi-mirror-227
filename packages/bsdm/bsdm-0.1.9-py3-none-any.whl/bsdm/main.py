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

from classes.Relation import Relation

from classes.Layout import Layout




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
    
    _dictDescription = json.loads(jsonDescription)
    
    ## BLOCKS
    # create blocks
    _blocks = {}
    
    for entity in _dictDescription['entities']:
    
        _eName = entity['name']
        _block = ETBlock(0, 0, _eName)
        
        # title
        _block.setTitle('TITLE '+_eName)
        
        # attributes
        if 'attributes' in entity:
            for attribute in entity['attributes']:
                _aId = False
                _aMandatory = False
                _aDeprecated = False
                
                _aName = attribute['name']
                
                if 'id' in attribute:
                    _aId = attribute['id']
            
                if 'mandatory' in attribute:
                    _aMandatory = attribute['mandatory']
        
                if 'deprecated' in attribute:
                    _aDeprecated = attribute['deprecated']

                _block.addAttr(_aName, _aId, _aMandatory, _aDeprecated)
        
        _block.build()
        _blocks[_eName] = _block
    
    # build layout
    Layout.spring(_dictDescription)

    # scale layout
    Layout.cleverScale(_blocks, 300) 
    
    # set blocks position
    for _blockName in _blocks:
        _vertice = Layout.getVertice(_blockName)        
        _blocks[_blockName].update(x=_vertice.getX(), y=_vertice.getY())
        
    
    ##LINES
    #create lines
    
    _relations = []
    
    for _relation in _dictDescription['relations']:
        
        _entity1 = _blocks[_relation['et1']]
        _width1 = _entity1.getWidth()
        _height1 = _entity1.getHeight()   
        _x1 = _entity1.getX() + _width1/2
        _y1 = _entity1.getY() + _height1/2

        _entity2 = _blocks[_relation['et2']]  
        _width2 = _entity2.getWidth()
        _height2 = _entity2.getHeight()    
        _x2 = _entity2.getX() + _width2/2
        _y2 = _entity2.getY() + _height2/2
        
        _relations.append(Relation(_x1, _y1, _width1, _height1, _x2, _y2, _width2, _height2))

    # finalize drawing

    for _blockName in _blocks:
        _blocks[_blockName].build()
        _blocks[_blockName].draw()

    for _relation in _relations:
        _relation.build()
        _relation.draw()


def bsdm():

    args = checkArgs()
    
    LOGGER.info('BSDM is not what you think!')
    LOGGER.info(args.css_file + ", " +  args.output_svg_file + ", " +  args.data_model)    

    outputSVGPath = setOutputSVGPath(args.output_svg_file)
    cssStyleSheet = getInputCSS(args.css_file)  
    
    Drawing.create(outputSVGPath, cssStyleSheet)

    jsonDescription = \
    '''
    {                                                       
        "entities" :                                         
        [                                                      
            {
                "name" : "A",
                "attributes" : 
                [
                    {"name" : "Kouroukoukou", "id":true, "mandatory":true, "deprecated":false},
                    {"name" : "attttribute attrt  attr", "id":false, "mandatory":false, "deprecated":true}
                ]
            },
            {"name" : "B"},
            {"name" : "C"}
        ],
        "relations" :
        [
            {"et1" : "A", "et2" : "B" },
            {"et1" : "B", "et2" : "C" },
            {"et1" : "C", "et2" : "A" }
        ]
    }
    '''
    
    buildFromJSONDescription(jsonDescription)

    Drawing.write()
    
    #_block.translate(400, 400)    
    
    #Drawing.reset()    



def main():
    bsdm()

if __name__ == "__main__":
    main()
    
    