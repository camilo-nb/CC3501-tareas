from numpy.random import randint
from OpenGL.GL import *

from data.mydata import d
import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.scene_graph as sg
import lib.transformations as tr

class Apple():
    
    def __init__(self):
        
        gpu_stem = es.toGPUShape(bs.createColorQuad(159/255, 107/255, 61/255))
        gpu_skin = es.toGPUShape(bs.create_circle(0.5, (0, 0), (1.0, 0.0, 0.0)))
        gpu_leaf = es.toGPUShape(bs.createColorQuad(0.0, 1.0, 0.0))
        
        stem = sg.SceneGraphNode("stem")
        stem.transform = tr.matmul([tr.uniformScale(0.5), tr.scale(0.5, 1, 1), tr.translate(0, 1, 0)])
        stem.childs += [gpu_stem]
        
        skin = sg.SceneGraphNode("skin")
        skin.transform = tr.matmul([tr.scale(1, 1, 1), tr.translate(0, 0, 0)])
        skin.childs += [gpu_skin]
        
        leaf = sg.SceneGraphNode("leaf")
        leaf.transform = tr.matmul([tr.uniformScale(0.5), tr.scale(1, 0.5, 1), tr.translate(0.25, 3, 0)])
        leaf.childs += [gpu_leaf]

        apple = sg.SceneGraphNode("apple")
        apple.transform = tr.matmul([tr.uniformScale(0.75), tr.scale(1/d["n"], 1/d["n"], 1), tr.scale(1, d["w"]/d["h"], 1)])
        apple.childs += [stem, skin, leaf]
        
        self.x, self.y = randint(0, d["n"]-2, 2)
        apple_tr = sg.SceneGraphNode('apple_tr')
        apple_tr.transform = tr.translate(self.x, self.y, 0)
        apple_tr.childs += [apple]

        self.model = apple_tr
        
        
    def draw(self, pipeline):
        if d["n"] % 2 == 0:
            self.model.transform = tr.translate((self.x - d["n"]//2 + 1 + 0.5)/d["n"], (self.y - d["n"]//2 + 1 + 0.5)/d["n"]*d["w"]/d["h"], 0)
        else:
            self.model.transform = tr.translate((self.x - d["n"]//2 + 2)/d["n"], (self.y - d["n"]//2 + 2)/d["n"]*d["w"]/d["h"], 0)
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

    def respawn(self, snake):
        self.x, self.y = randint(0, d["n"]-2, 2)
        if snake.time - snake.grid[self.y][self.x] < snake.length:
            return self.respawn(snake)