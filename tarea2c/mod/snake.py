import os
from collections import deque

import numpy as np
from OpenGL.GL import *

import lib.easy_shaders as es
import lib.transformations as tr
import lib.object_handler as oh

class Head():
    
    def __init__(self):
        self.x, self.y, self.z = 0, 0, 1 # position coordinates
        self.rho, self.phi = 0.2, 0 # direction vector
        self.bend = np.pi/180*2 # how much to bend when turning
        self.turn = 0 # -1:right, 0:straight, 1:left
        self.time = 0
        self.s = 2 # separation
        self.GPU = es.toGPUShape(oh.readOBJ2(os.path.join('mod','tex','pokeball.obj'), os.path.join('mod','tex','pokeball.png')), GL_REPEAT, GL_NEAREST)
        self.transform = np.matmul(np.matmul(tr.translate(*self.pos), tr.uniformScale(self.s/2)), tr.rotationZ(self.phi))
    @property
    def pos(self): return self.x, self.y, self.z
    
    def draw(self, pipeline, projection, view):
        glUseProgram(pipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 0.55, 0.55, 0.55)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 0.65, 0.65, 0.65)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.4, 0.4, 0.4)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.25, 0.25, 0.25)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.6, 0.6, 0.6)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.6, 0.6, 0.6)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 50,50 ,50)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), *self.pos)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 100000)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPU)
        
    def turn_right(self): self.turn = -1
    def turn_straight(self): self.turn = 0
    def turn_left(self): self.turn = 1
    def turn_steering_wheel(self): self.phi += self.bend * self.turn
    def move_forward(self):
        self.time += self.bend / (self.rho * self.s)
        self.x += self.rho * np.cos(self.phi)
        self.y += self.rho * np.sin(self.phi)
        self.transform = tr.matmul([
            tr.translate(self.x,self.y,self.z),
            tr.uniformScale(self.s/2),
            tr.rotationA(self.time*self.s,np.array([np.cos(self.phi+np.pi/2),np.sin(self.phi+np.pi/2),0])),
            tr.rotationZ(self.phi)
        ])
        
    def update(self):
        self.move_forward()
        self.turn_steering_wheel()
    
class Snake():
    
    def __init__(self):
        self.alive = True
        self.head = Head()
        #self.body = deque()
        #self.body.append(Head())
        self.length = 1
    #@property
    #def head(self): return self.body[0]
    @property
    def x(self): return self.head.x
    @property
    def y(self): return self.head.y
    @property
    def z(self): return self.head.z
    @property
    def rho(self): return self.head.rho
    @property
    def phi(self): return self.head.phi
    @property
    def tail(self): return self.body[-1]
    
    def draw(self, pipeline, projection, view):
        if not self.alive: return
        self.head.draw(pipeline, projection, view)
        #for part in self.body: part.draw(pipeline, projection, view)

    def turn_right(self): self.head.turn_right()
    def turn_straight(self): self.head.turn_straight()
    def turn_left(self): self.head.turn_left()
    def slither(self):
        if not self.alive: return
        self.head.update()
        #new_head = Head()
        #new_head.pos = self.head.pos
        #new_head.pol = self.head.pol
        #self.body.appendleft(new_head)
        #self.head.update()
        #_=self.body.pop()
        
    def update(self):
        self.slither()