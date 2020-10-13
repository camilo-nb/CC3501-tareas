import os

import numpy as np
from PIL import Image
from OpenGL.GL import *

from data.mydata import d
import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.scene_graph as sg
import lib.transformations as tr

class Chessboard():
    
    def __init__(self, n):
        gpu_chessboard = es.chessboard2GPUShape(bs.createChessboard(), n)
        
        chessboard = sg.SceneGraphNode("chessboard")
        chessboard.transform = tr.scale(1, d["w"]/d["h"], 1)
        chessboard.childs += [gpu_chessboard]
        
        chessboard_tr = sg.SceneGraphNode("chessboardTR")
        chessboard_tr.transfrom = tr.identity()
        chessboard_tr.childs += [chessboard]

        self.model = chessboard_tr

                    
    def draw(self, pipeline):
        self.model.transform = tr.translate(0, 0, 0)
        sg.drawSceneGraphNode(self.model, pipeline, "transform")