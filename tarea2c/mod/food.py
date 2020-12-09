import os

import numpy as np
from OpenGL.GL import *
import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr
import lib.object_handler as oh

class Charmander():
    def __init__(self): self.GPU = es.toGPUShape(oh.readOBJ(os.path.join('mod','tex','charmander.obj'), (241/255, 95/266, 62/255)), GL_REPEAT, GL_NEAREST)
    def draw(self, pipeline, projection, view, transform, view_pos):
        glUseProgram(pipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 241/255, 95/266, 62/255)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 241/255, 95/266, 62/255)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 241/255, 95/266, 62/255)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.1, 0.1, 0.1)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 50, 50, 50)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), *view_pos)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 10000)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPU)
class Bulbasaur():
    def __init__(self): self.GPU = es.toGPUShape(oh.readOBJ(os.path.join('mod','tex','bulbasaur.obj'), (137/255, 200/255, 147/255)), GL_REPEAT, GL_NEAREST)
    def draw(self, pipeline, projection, view, transform, view_pos):
        glUseProgram(pipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 137/255, 200/255, 147/255)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 137/255, 200/255, 147/255)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 137/255, 200/255, 147/255)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.1, 0.1, 0.1)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 50, 50, 50)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), *view_pos)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 10000)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPU)
class Squirtle():
    def __init__(self): self.GPU = es.toGPUShape(oh.readOBJ(os.path.join('mod','tex','squirtle.obj'), (162/255, 215/255, 213/255)), GL_REPEAT, GL_NEAREST)
    def draw(self, pipeline, projection, view, transform, view_pos):
        glUseProgram(pipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 162/255, 215/255, 213/255)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 162/255, 215/255, 213/255)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 162/255, 215/255, 213/255)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.1, 0.1, 0.1)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 50, 50, 50)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), *view_pos)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 10000)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPU)
class Pikachu():
    def __init__(self): self.GPU = es.toGPUShape(oh.readOBJ(os.path.join('mod','tex','pikachu.obj'), (250/255, 214/255, 29/255)), GL_REPEAT, GL_NEAREST)
    def draw(self, pipeline, projection, view, transform, view_pos):
        glUseProgram(pipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 250/255, 214/255, 29/255)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 250/255, 214/255, 29/255)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 250/255, 214/255, 29/255)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.1, 0.1, 0.1)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), *view_pos)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), *view_pos)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 10000000)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPU)

class Food():
    
    def __init__(self):
        self.x, self.y = 0, 0
        self.z = 1
        self.time = 0
        self.tick = np.pi/180*2
        self.s = 3
        self.models = {
            'charmander' : Charmander(),
            'bulbasaur' : Bulbasaur(),
            'squirtle' : Squirtle(),
            'pikachu' : Pikachu()
        }
        self.list = ['charmander', 'bulbasaur', 'squirtle', 'pikachu']
        self.prob = [0.3, 0.3, 0.3, 0.1]
        self.choice_model()
        self.transform = np.matmul(tr.translate(self.x,self.y,self.z), np.matmul(tr.rotationZ(self.time*4), np.matmul(tr.rotationX(np.pi/2), tr.uniformScale(self.s))))
    
    def choice_model(self):
        self.status = np.random.choice(self.list, p=self.prob)
        self.model = self.models[self.status]
    
    def draw(self, pipeline, projection, view):
        self.model.draw(pipeline, projection, view, self.transform, (self.x, self.y, self.z))
    
    def update(self):
        self.time += self.tick
        self.z = np.exp(2*np.sin(2*self.time))/4
        self.transform = np.matmul(tr.translate(self.x,self.y,self.z), np.matmul(tr.rotationZ(self.time*4), np.matmul(tr.rotationX(np.pi/2), tr.uniformScale(self.s))))        
   
    def respawn(self, snake, obstacle):
        self.choice_model()
        x, y = self.x, self.y; self.x, self.y = np.random.uniform(-97.9, 97.9, 2)
        if (self.x - x)**2 + (self.y - y)**2 < self.s**2: self.respawn(snake, obstacle); return
        if (self.x - obstacle.x)**2 + (self.y - obstacle.x)**2 < self.s**2: self.respawn(snake, obstacle); return
        parts = iter(snake.body); _=next(parts,None)
        for part in parts:
            if (self.x - part.x)**2 + (self.y - part.y)**2 < self.s**2: self.respawn(snake, obstacle); return
        self.transform = np.matmul(tr.translate(self.x,self.y,self.z), np.matmul(tr.rotationZ(self.time*4), np.matmul(tr.rotationX(np.pi/2), tr.uniformScale(self.s))))
