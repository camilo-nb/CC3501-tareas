import os

import numpy as np
from OpenGL.GL import *

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr

class Snake():
    
    def __init__(self):
        self.x, self.y = 0, 0
        self.theta = 0
        self.bend = np.pi/2/4
        self.front = 0.01
        self.GPU = es.toGPUShape(bs.createTextureCube(os.path.join('model','snake.png')), GL_REPEAT, GL_LINEAR)
        self.transform = tr.matmul([tr.translate(0,0,-20),tr.uniformScale(20)])
    
    def draw(self, texture_pipeline, projection, view):
        glUseProgram(texture_pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        texture_pipeline.drawShape(self.GPU)
    def turn_left(self): self.theta += self.bend
    def turn_right(self): self.theta -= self.bend
    def move(self):
        self.x += self.front*np.cos(self.theta)
        self.y += self.front*np.sin(self.theta)
        self.transform = tr.matmul([tr.translate(self.x,self.y,10),tr.uniformScale(1)])
    def update(self):
        self.move()
        