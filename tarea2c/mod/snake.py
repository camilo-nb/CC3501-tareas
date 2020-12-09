import os
from copy import deepcopy
from collections import deque

import numpy as np
from OpenGL.GL import *

import lib.easy_shaders as es
import lib.transformations as tr
import lib.object_handler as oh

class Pokeball():
    
    def __init__(self):
        self.x, self.y, self.z = -99, 0, 1 # position coordinates
        self.rho, self.phi = 0.01, 0 # direction vector
        self.bend = np.pi/180*2*2*2 # how much to bend when turning
        self.turn = 0 # -1:right, 0:straight, 1:left
        self.time = 0
        self.s = 2 # scale
        self.GPU = es.toGPUShape(oh.readOBJ2(os.path.join('mod','tex','pokeball.obj'), os.path.join('mod','tex','pokeball.png')), GL_REPEAT, GL_NEAREST)
        self.transform = np.matmul(np.matmul(tr.translate(*self.pos), tr.uniformScale(self.s/2)), tr.rotationZ(self.phi))
    @property
    def pos(self): return self.x, self.y, self.z
    
    def draw(self, pipeline, projection, view, food):
        if food.status == 'pikachu': light_pos = [food.x, food.y, food.z]; shininess = 1
        else: light_pos = [50, 50, 50]; shininess = 10000
        glUseProgram(pipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 0.6, 0.6, 0.6)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.8, 0.8, 0.8)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.4, 0.4, 0.4)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.6, 0.6, 0.6)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.8, 0.8, 0.8)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), *light_pos)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), *self.pos)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), shininess)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.00001)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPU)
        
    def turn_right(self): self.turn = -1
    def turn_straight(self): self.turn = 0
    def turn_left(self): self.turn = 1
    def turn_steering_wheel(self): self.phi += self.bend * self.turn
    def move_forward(self):
        #self.time += self.bend / (self.rho * self.s)
        self.time += self.bend
        self.x += self.rho * np.cos(self.phi)
        self.y += self.rho * np.sin(self.phi)
        self.transform = tr.matmul([
            tr.translate(self.x,self.y,self.z),
            tr.uniformScale(self.s/2),
            tr.rotationA(self.time*self.s,np.array([np.cos(self.phi+np.pi/2),np.sin(self.phi+np.pi/2),0])),
            tr.rotationZ(self.phi)
        ])
        
    def ahead(self):
        #self.time += self.bend / (self.rho * self.s)
        self.time += self.bend
        self.x += self.s * np.cos(self.phi)
        self.y += self.s * np.sin(self.phi)
        self.transform = tr.matmul([
            tr.translate(self.x,self.y,self.z),
            tr.uniformScale(self.s/2),
            tr.rotationA(self.time*self.s,np.array([np.cos(self.phi+np.pi/2),np.sin(self.phi+np.pi/2),0])),
            tr.rotationZ(self.phi)
        ])
        #self.turn_steering_wheel()
        
    def update(self):
        self.move_forward()
        self.turn_steering_wheel()
    
class Snake():
    
    def __init__(self):
        self.alive = True
        self.head = Pokeball()
        self.body = deque()
        self.length = 1
        self.time = 0
        self.init_tail = 0
        while self.init_tail:
            self.grow()
            self.init_tail -= 1
    #@property
    #def head(self): return self.body[0]
    @property
    def x(self): return self.head.x
    @property
    def y(self): return self.head.y
    @property
    def z(self): return self.head.z
    @z.setter
    def z(self, value): self.head.z = value
    @property
    def rho(self): return self.head.rho
    @property
    def phi(self): return self.head.phi
    @property
    def tail(self): return self.body[-1]
    
    def draw(self, pipeline, projection, view, food):
        #if not self.alive: return
        self.head.draw(pipeline, projection, view, food)
        for part in self.body: part.draw(pipeline, projection, view, food)

    def turn_right(self): self.head.turn_right()
    def turn_straight(self): self.head.turn_straight()
    def turn_left(self): self.head.turn_left()
    def slither(self):
        if not self.alive: return
        self.head.update()
        self.body.appendleft(deepcopy(self.head))
        self.head.ahead()
        self.body.pop()
        if self.body:
            i = self.length
            while i := i-1:
                part = self.body.popleft(); part.update()
                self.body.append(part)

    def grow(self):
        if not self.alive: return
        self.body.appendleft(deepcopy(self.head))
        self.head.ahead()
        self.length += 1
    
    def food_collide(self, food, obstacle):
        if abs(self.x - food.x) < self.head.s and abs(self.y - food.y) < self.head.s:
            self.grow()
            food.respawn(self, obstacle)
            
    def self_collide(self):
        parts = iter(self.body)
        _=next(parts,None)
        for part in parts:
            if (self.head.x - part.x)**2 + (self.head.y - part.y)**2 < self.head.s:
                self.die()

    def border_collide(self):
        if abs(self.x) > 100 or abs(self.y) > 100:
            self.die()
    
    def obstacle_collide(self, obstacle):
        if abs(self.x - obstacle.x) < obstacle.s*1.1 and abs(self.y - obstacle.y) < obstacle.s*1.1:
            self.die()
    
    def fall(self):
        if self.alive: return
        self.dead_since += 1
        self.z  = self.z - (1-np.exp(-self.dead_since))
    
    def die(self):
        self.alive = False
        self.dead_since = 0
    
    def update(self, food, obstacle):
        self.time += 1
        if self.time < 200: return
        self.food_collide(food, obstacle)
        self.self_collide()
        self.border_collide()
        self.obstacle_collide(obstacle)
        self.slither()
        self.fall()