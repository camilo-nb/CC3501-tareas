import os

from OpenGL.GL import *

from data.mydata import d
import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.scene_graph as sg
import lib.transformations as tr

class GameOver():
    
    def __init__(self):
        
        path = os.path.join("model", "gameover.png")
        gpu_gameover = es.toGPUShape(bs.createTextureQuad(path), GL_REPEAT, GL_NEAREST)
        
        gameover = sg.SceneGraphNode("gameover")
        gameover.transform = tr.scale(1, d["w"]/d["h"], 1)
        gameover.childs = [gpu_gameover]
        
        gameover_r = sg.SceneGraphNode("gameover_r")
        gameover_r.childs += [gameover]
        
        self.model = gameover_r
        self.phi = 0
        
    def draw(self, pipeline):
        self.model.transform = tr.matmul([tr.rotationX(2 * self.phi), tr.rotationZ(self.phi)])
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
        
    def update(self, dt):
        self.phi += dt
        