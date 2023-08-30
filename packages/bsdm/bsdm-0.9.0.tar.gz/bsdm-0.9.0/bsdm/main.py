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
        epilog='Generate SVG beautiful diagram with CSS from json or Oracle Data Modeler.')

    parser.add_argument('-c','--css_file', required=False, help='css filename')
    parser.add_argument('data_model', help='Data Model file or directory')
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


def getDataModel(data_model):
    
    if(data_model):
        _data_model = data_model
    else :
        return None
    
    _data_model = Path(_data_model).resolve()

    if(_data_model.exists() and _data_model.is_file()):
        with open(str(_data_model), "r", encoding="utf-8") as _data_model :
            return _data_model.read() 

    LOGGER.error('Problem with data model file. Abort.')
    exit(-1)

def buildFromJSONDescription(jsonDescription):
    
    _dictDescription = json.loads(jsonDescription)
    
    Drawing.setSize( (len(_dictDescription['entities']) * 200, len(_dictDescription['entities']) * 200) )
    Drawing.reset()
    
    ## BLOCKS
    # create blocks
    _blocks = {}
    
    for entity in _dictDescription['entities']:
    
        _eName = entity['name']
        _block = ETBlock(0, 0, _eName)
        
        # title
        if 'title' in entity:
            _eTitle = entity['title']
        else:
            _eTitle = 'TITLE '+_eName
        
        _block.setTitle(_eTitle)
        
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
    #Layout.cleverScale(_blocks,  15 * (len(_dictDescription['entities']) ** 2 )) 
    Layout.scale(20 * (len(_dictDescription['entities']) ** 2 ) ) 
    
    # set blocks position
    for _blockName in _blocks:
        _vertice = Layout.getVertice(_blockName)        
        _blocks[_blockName].update(x=_vertice.getX(), y=_vertice.getY())
        
    
    ##LINES
    #create lines
    
    _relations = []
    
    for _relation in _dictDescription['relations']:
        
        _entity1 = _blocks[_relation['et1']]
        _entity1Card = "one"
        if 'et1card' in _relation:
            _entity1Card = _relation['et1card']
        _entity1Mandatory = True
        if 'et1mandatory' in _relation:
            _entity1Mandatory = _relation['et1mandatory']
        _entity1RelName = None
        if 'et1relname' in _relation:
            _entity1RelName = _relation['et1relname']

        _entity2 = _blocks[_relation['et2']]  
        _entity2Card = "one"
        if 'et2card' in _relation:
            _entity2Card = _relation['et2card']
        _entity2Mandatory = True
        if 'et2mandatory' in _relation:
            _entity2Mandatory = _relation['et2mandatory']
        _entity2RelName = None
        if 'et2relname' in _relation:
            _entity2RelName = _relation['et2relname']
        
        _relations.append(Relation(_entity1, _entity2, _entity1Card, _entity2Card, _entity1Mandatory, _entity2Mandatory, _entity1RelName, _entity2RelName, hvLines=True))

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
    data_model =  getDataModel(args.data_model) 
    
    Drawing.create(outputSVGPath, cssStyleSheet=cssStyleSheet)

    jsonDescription = data_model
    
    buildFromJSONDescription(jsonDescription)

    Drawing.write()
    
    #_block.translate(400, 400)    
    
    #Drawing.reset()    



def main():
    bsdm()

if __name__ == "__main__":
    main()
    
    