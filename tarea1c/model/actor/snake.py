import os

import numpy as np
from OpenGL.GL import *

from data.mydata import d
import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.scene_graph as sg
import lib.transformations as tr

class SnakePart():
    
    def __init__(self, path):
        
        gpu_part = es.toGPUShape(bs.createTextureQuad(path), GL_REPEAT, GL_NEAREST)

        part = sg.SceneGraphNode("part")
        part.transform = tr.matmul([tr.scale(1, d["w"]/d["h"], 1), tr.scale(1/d["n"], 1/d["n"], 1)])
        part.childs += [gpu_part]
        
        part_tr = sg.SceneGraphNode("part_tr")
        part_tr.transform = tr.identity()
        part_tr.childs += [part]
        
        self.model = part_tr
        
    @staticmethod
    def green(cls):
        return cls(os.path.join("model", "actor", "green.png"))
    
    @staticmethod
    def head(cls, n):
        return cls(os.path.join("model", "actor", "head_"+str(n)+".png"))
    
    @staticmethod
    def body(cls):
        return cls(os.path.join("model", "actor", "body.png"))
    
    @staticmethod
    def curve(cls):
        return cls(os.path.join("model", "actor", "curve.png"))

class Snake():
    
    def __init__(self):
        
        self.is_alive = True
        self.f = False
        self.r = False
        self.time = 0
        self.length = 1
        self.x = 0
        self.y = 0
        self.dx = 1
        self.dy = 0
        self.ddx = 1
        self.ddy = 0
        
        self.grid = np.full((d["n"], d["n"]), -1, dtype=int)
        self.grid[self.y][self.x] = self.time
        
        self.green = SnakePart.green(SnakePart)
        self.head0 = SnakePart.head(SnakePart,0)
        self.head1 = SnakePart.head(SnakePart,1)
        self.head2 = SnakePart.head(SnakePart,2)
        self.head3 = SnakePart.head(SnakePart,3)
        self.head = None
        self.body = SnakePart.body(SnakePart)
        self.curve = SnakePart.curve(SnakePart)
        
    def draw(self, pipeline, apple):
        
        for j in range(len(self.grid)):
            for i in range(len(self.grid)):
                
                if self.grid[j][i] < 0:
                    continue
                
                elif self.time - self.grid[j][i] < self.length:
                    
                    if abs(apple.x - self.x) < 2 and abs(apple.y - self.y) < 2:
                        self.head = self.head3
                    elif abs(apple.x - self.x) < 3 and abs(apple.y - self.y) < 3:
                        self.head = self.head2
                    elif abs(apple.x - self.x) < 4 and abs(apple.y - self.y) < 4:
                        self.head = self.head1
                    else:
                        self.head = self.head0
                    
                    # head
                    if self.grid[j][i] == self.time:
                        
                        # down
                        if self.ddx == 0 and self.ddy == -1:
                            if d["n"] % 2 == 0:
                                self.head.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1 + 0.5)/d["n"], (j-d["n"]//2 + 1 + 0.5)/d["n"]*d["w"]/d["h"], 0),
                                        #tr.scale(d["h"]/d["w"], 1, 1),
                                        tr.translate(0,0,0)
                                    ]
                                    
                                    )
                            else:
                                self.head.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1)/d["n"], (j-d["n"]//2 + 1)/d["n"]*d["w"]/d["h"], 0),
                                        #tr.scale(d["h"]/d["w"], 1, 1),
                                        tr.translate(0,0,0)
                                    ]
                                )
                            sg.drawSceneGraphNode(self.head.model, pipeline, "transform")
                        
                        # right
                        elif self.ddx == 1 and self.ddy == 0:
                            if d["n"] % 2 == 0:
                                self.head.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1 + 0.5)/d["n"], (j-d["n"]//2 + 1 + 0.5)/d["n"]*d["w"]/d["h"], 0),
                                        tr.rotationZ(np.pi/2),
                                        tr.scale(d["w"]/d["h"], d["h"]/d["w"], 1),
                                        tr.translate(0,0,0)
                                    ]
                                )
                            else:
                                self.head.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1)/d["n"], (j-d["n"]//2 + 1)/d["n"]*d["w"]/d["h"], 0),
                                        tr.rotationZ(np.pi/2),
                                        tr.scale(d["w"]/d["h"], d["h"]/d["w"], 1),
                                        tr.translate(0,0,0)
                                    ]
                                )
                            sg.drawSceneGraphNode(self.head.model, pipeline, "transform")
                        
                        # up
                        elif self.ddx == 0 and self.ddy == 1:
                            if d["n"] % 2 == 0:
                                self.head.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1 + 0.5)/d["n"], (j-d["n"]//2 + 1 + 0.5)/d["n"]*d["w"]/d["h"], 0),
                                        tr.rotationZ(np.pi),
                                        #tr.scale(d["h"]/d["w"], 1, 1),
                                        tr.translate(0,0,0)
                                    ]
                                )
                            else:
                                self.head.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1)/d["n"], (j-d["n"]//2 + 1)/d["n"]*d["w"]/d["h"], 0),
                                        tr.rotationZ(np.pi),
                                        #tr.scale(d["h"]/d["w"], 1, 1),
                                        tr.translate(0,0,0)
                                    ]
                                )
                                
                            sg.drawSceneGraphNode(self.head.model, pipeline, "transform")

                        # left
                        elif self.ddx == -1 and self.ddy == 0:
                            if d["n"] % 2 == 0:
                                self.head.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1 + 0.5)/d["n"], (j-d["n"]//2 + 1 + 0.5)/d["n"]*d["w"]/d["h"], 0),
                                        tr.rotationZ(3*np.pi/2),
                                        tr.scale(d["w"]/d["h"], d["h"]/d["w"], 1),
                                        tr.translate(0,0,0)
                                    ]
                                )
                            else:
                                self.head.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1)/d["n"], (j-d["n"]//2 + 1)/d["n"]*d["w"]/d["h"], 0),
                                        tr.rotationZ(3*np.pi/2),
                                        tr.scale(d["w"]/d["h"], d["h"]/d["w"], 1),
                                        tr.translate(0,0,0)
                                    ]
                                )
                                
                            sg.drawSceneGraphNode(self.head.model, pipeline, "transform")
                        
                    else:
                        
                        # vertical body
                        if 0 < j < d["n"] - 3 and (self.grid[j][i] == self.grid[j+1][i]+1 and self.grid[j][i] == self.grid[j-1][i]-1) or \
                            (self.grid[j][i] == self.grid[j+1][i]-1 and self.grid[j][i] == self.grid[j-1][i]+1):
                            if d["n"] % 2 == 0:
                                self.body.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1 + 0.5)/d["n"], (j-d["n"]//2 + 1 + 0.5)/d["n"]*d["w"]/d["h"], 0),
                                        #tr.scale(d["h"]/d["w"], 1, 1),
                                        tr.translate(0,0,0)
                                    ]
                                )
                                  
                            else:
                                self.body.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1)/d["n"], (j-d["n"]//2 + 1)/d["n"]*d["w"]/d["h"], 0),
                                        #tr.scale(d["h"]/d["w"], 1, 1),
                                        tr.translate(0,0,0)
                                    ]
                                )
                                
                            sg.drawSceneGraphNode(self.body.model, pipeline, "transform")

                        # horizontal body
                        elif 0 < i < d["n"] - 3 and (self.grid[j][i] == self.grid[j][i+1]+1 and self.grid[j][i] == self.grid[j][i-1]-1) or \
                            (self.grid[j][i] == self.grid[j][i+1]-1 and self.grid[j][i] == self.grid[j][i-1]+1):
                            if d["n"] % 2 == 0:
                                self.body.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1 + 0.5)/d["n"], (j-d["n"]//2 + 1 + 0.5)/d["n"]*d["w"]/d["h"], 0),
                                        tr.rotationZ(np.pi/2),
                                        tr.scale(d["w"]/d["h"], d["h"]/d["w"], 1),
                                        tr.translate(0,0,0)
                                    ]
                                )
                            else:
                                self.body.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1)/d["n"], (j-d["n"]//2 + 1)/d["n"]*d["w"]/d["h"], 0),
                                        tr.rotationZ(np.pi/2),
                                        tr.scale(d["w"]/d["h"], d["h"]/d["w"], 1),
                                        tr.translate(0,0,0)
                                    ]
                                )
                            sg.drawSceneGraphNode(self.body.model, pipeline, "transform")
                        
                        # top left curve
                        elif 0 < i and j < d["n"] - 3 and (self.grid[j][i] == self.grid[j+1][i]+1 and self.grid[j][i] == self.grid[j][i-1]-1) or \
                            (self.grid[j][i] == self.grid[j+1][i]-1 and self.grid[j][i] == self.grid[j][i-1]+1):
                            if d["n"] % 2 == 0:
                                self.curve.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1 + 0.5)/d["n"], (j-d["n"]//2 + 1 + 0.5)/d["n"]*d["w"]/d["h"], 0),
                                        tr.rotationZ(np.pi),
                                        tr.translate(0,0,0)
                                    ]
                                )
                            else:
                                self.curve.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1)/d["n"], (j-d["n"]//2 + 1)/d["n"]*d["w"]/d["h"], 0),
                                        tr.rotationZ(np.pi),
                                        tr.translate(0,0,0)
                                    ]
                                )
                            sg.drawSceneGraphNode(self.curve.model, pipeline, "transform")
                            
                        # top right curve
                        elif i < d["n"] - 3 and j < d["n"] - 3 and (self.grid[j][i] == self.grid[j+1][i]+1 and self.grid[j][i] == self.grid[j][i+1]-1) or \
                            (self.grid[j][i] == self.grid[j+1][i]-1 and self.grid[j][i] == self.grid[j][i+1]+1):
                            if d["n"] % 2 == 0:
                                self.curve.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1 + 0.5)/d["n"], (j-d["n"]//2 + 1 + 0.5)/d["n"]*d["w"]/d["h"], 0),
                                        tr.rotationZ(np.pi/2),
                                        tr.scale(d["w"]/d["h"], d["h"]/d["w"], 1),
                                        tr.translate(0,0,0)
                                    ]
                                )
                            else:
                                self.curve.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1)/d["n"], (j-d["n"]//2 + 1)/d["n"]*d["w"]/d["h"], 0),
                                        tr.rotationZ(np.pi/2),
                                        tr.scale(d["w"]/d["h"], d["h"]/d["w"], 1),
                                        tr.translate(0,0,0)
                                    ]
                                )
                            sg.drawSceneGraphNode(self.curve.model, pipeline, "transform")

                        # bottom left curve
                        elif 0 < i and 0 < j and (self.grid[j][i] == self.grid[j-1][i]+1 and self.grid[j][i] == self.grid[j][i-1]-1) or \
                            (self.grid[j][i] == self.grid[j-1][i]-1 and self.grid[j][i] == self.grid[j][i-1]+1):
                            if d["n"] % 2 == 0:
                                self.curve.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1 + 0.5)/d["n"], (j-d["n"]//2 + 1 + 0.5)/d["n"]*d["w"]/d["h"], 0),
                                        tr.rotationZ(3*np.pi/2),
                                        tr.scale(d["w"]/d["h"], d["h"]/d["w"], 1),
                                        tr.translate(0,0,0)
                                    ]
                                )
                            else:
                                self.curve.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1)/d["n"], (j-d["n"]//2 + 1)/d["n"]*d["w"]/d["h"], 0),
                                        tr.rotationZ(3*np.pi/2),
                                        tr.scale(d["w"]/d["h"], d["h"]/d["w"], 1),
                                        tr.translate(0,0,0)
                                    ]
                                )
                            sg.drawSceneGraphNode(self.curve.model, pipeline, "transform")
                            
                        # bottom right curve
                        elif i < d["n"] - 3 and 0 < j and (self.grid[j][i] == self.grid[j-1][i]+1 and self.grid[j][i] == self.grid[j][i+1]-1) or \
                            (self.grid[j][i] == self.grid[j-1][i]-1 and self.grid[j][i] == self.grid[j][i+1]+1):
                            if d["n"] % 2 == 0:
                                self.curve.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1 + 0.5)/d["n"], (j-d["n"]//2 + 1 + 0.5)/d["n"]*d["w"]/d["h"], 0),
                                    ]
                                )
                                
                                
                            else:
                                self.curve.model.transform = tr.matmul(
                                    [
                                        tr.translate((i-d["n"]//2 + 1)/d["n"], (j-d["n"]//2 + 1)/d["n"]*d["w"]/d["h"], 0)
                                    ]
                                )
                                
                            sg.drawSceneGraphNode(self.curve.model, pipeline, "transform")

                        else:
                            if d["n"] % 2 == 0:
                                self.green.model.transform = tr.translate((i-d["n"]//2 + 1 + 0.5)/d["n"], (j-d["n"]//2 + 1 + 0.5)/d["n"]*d["w"]/d["h"], 0)
                            else:
                                self.green.model.transform = tr.translate((i-d["n"]//2 + 1)/d["n"], (j-d["n"]//2 + 1)/d["n"]*d["w"]/d["h"], 0)
                            sg.drawSceneGraphNode(self.green.model, pipeline, "transform")
        self.ddx = self.dx
        self.ddy = self.dy
        
    def die(self):
        d.load()
        try:
            if d["s"]:
                try:
                    from lib.playsound import playsound
                except KeyError:
                    d["s"] = True
                    d.dump()      
                else:
                    playsound(os.path.join("data", "doh.mp3"), block=False)
        except KeyError:
            d["s"] = False
            d.dump()
        self.x, self.y = 0, 0
        self.length = 1
        self.is_alive = False
        
    def tick(self):
        self.time += 1
        self.grid[self.y][self.x] = self.time
       
    def move(self):
        self.x += self.dx
        self.y += self.dy
            
    def apple_collide(self, apple):
        if self.x == apple.x and self.y == apple.y:
            d.load()
            try:
                if d["s"]:
                    try:
                        from lib.playsound import playsound
                    except KeyError:
                        d["s"] = True
                        d.dump()      
                    else:
                        playsound(os.path.join("data", "mmm.mp3"), block=False)
            except KeyError:
                d["s"] = False
                d.dump()
            apple.respawn(self)
            self.length += 1
            
    def border_collide(self):
        if self.x < 0 or self.x > d["n"]-3 or self.y < 0 or self.y > d["n"]-3:
            self.die()
            
    def self_collide(self):
        if self.time - self.grid[self.y][self.x] < self.length:
            self.die()
        
    def update(self, apple):
        self.tick()
        self.move()
        self.apple_collide(apple)
        self.border_collide()
        self.self_collide()