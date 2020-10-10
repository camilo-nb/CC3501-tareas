import os

from lib import scene_graph as sg
from lib import easy_shaders as es
from lib import basic_shapes as bs
from lib import transformations as tr
from OpenGL.GL import *

from data.data import data

class Snake():
    
    def __init__(self):
        face_path = os.path.join("src", "models", "actor", "face.png")
        gpu_face = es.toGPUShape(bs.createTextureQuad(face_path), GL_REPEAT, GL_LINEAR)
        
        face = sg.SceneGraphNode("face")
        ratio = data["width"]/data["height"]
        face.transform = tr.scale(1, ratio, 1)
        face.childs += [gpu_face]
        
        snake = sg.SceneGraphNode('snake')
        snake.transform = tr.identity()
        snake.childs += [face]
        
        transform_snake = sg.SceneGraphNode('snakeTR')
        transform_snake.transform = tr.scale(0.5, 0.5, 1)
        transform_snake.childs += [snake]
        
        self.model = transform_snake
        self.posx = 0
        self.posy = 0
        self.velx = 1
        self.vely = 0
        self.accx = 0
        self.accy = 0
        self.last_mov = "d"
        self.new_mov = None
        
    def draw(self, pipeline):
        self.model.transform = tr.translate(self.posx, self.posy, 0)
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')
        
    def update(self, dt):
        self.move()
        self.velx += self.accx*dt
        self.vely += self.accy*dt
        self.posx += self.velx*dt
        self.posy += self.vely*dt
    
    def move_w(self):
        self.posx = int(self.posx)
        self.velx = 0
        self.vely = 1
        self.accx = 0
        self.accy = 0.1
    
    def move_a(self):
        self.posy = int(self.posy)
        self.velx = -1
        self.vely = 0
        self.accx = 0.1
        self.accy = 0
        
    def move_s(self):
        self.posx = int(self.posx)
        self.velx = 0
        self.vely = -1
        self.accx = 0
        self.accy = 0.1
        
    def move_d(self):
        self.posy = int(self.posy)
        self.velx = 1
        self.vely = 0
        self.accx = 0.1
        self.accy = 0
        
    def move(self):
        print(abs(int(self.posx) - self.posx))
        if self.new_mov == "w" and abs(int(self.posx) - self.posx) < 0.01 and not self.last_mov == "s":
            self.move_w()
            self.last_mov = self.new_mov

        elif self.new_mov == "a" and abs(int(self.posy) - self.posy) < 0.01 and not self.last_mov == "d":
            self.move_a()
            self.last_mov = self.new_mov
            
        elif self.new_mov == "s" and abs(int(self.posx) - self.posx) < 0.01 and not self.last_mov == "w":
            self.move_s()
            self.last_mov = self.new_mov
            
        elif self.new_mov == "d" and abs(int(self.posy) - self.posy) < 0.01 and not self.last_mov == "a":
            self.move_d()
            self.last_mov = self.new_mov
        
            
     
        
    # def move_w(self):
    #     self.vely = self.velx
    #     self.vely = -1*self.vely if self.vely < 0 else self.vely
    
    # def move_a(self):
    #     self.velx = -1*self.velx if self.velx > 0 else self.velx
        
    # def move_s(self):
    #     self.vely = -1*self.vely if self.vely > 0 else self.vely
        
    # def move_d(self):
    #     self.velx = -1*self.velx if self.velx < 0 else self.velx

    