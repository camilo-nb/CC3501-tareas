import os

import numpy as np
from OpenGL.GL import *

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr

class Food():
    
    def __init__(self):
        self.x, self.y = np.random.randint(-25, 25, 2)
        self.z = 1
        self.s = 1
        self.GPU = es.toGPUShape(bs.createTextureCube(os.path.join('mod','tex','food.png')), GL_REPEAT, GL_LINEAR)
        self.transform = tr.matmul([tr.translate(self.x,self.y,self.z),tr.uniformScale(self.s)])
        
    def draw(self, texture_pipeline, projection, view):
        glUseProgram(texture_pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        texture_pipeline.drawShape(self.GPU)
    
    def respawn(self, snake):
        self.x, self.y = np.random.randint(-25, 25, 2)
        self.transform = tr.matmul([tr.translate(self.x,self.y,self.z),tr.uniformScale(self.s)])
        parts = iter(snake.body)
        _=next(parts,None)
        for part in parts:
            if (self.x - part.x)**2 + (self.y - part.y)**2 < snake.head.s:
                self.respawn(snake)