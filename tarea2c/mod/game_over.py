import os
from collections import deque

import numpy as np
from OpenGL.GL import *

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr

class GameOver:
    def __init__(self):
        self.GPU = deque([
            es.toGPUShape(bs.createTextureCube(os.path.join('mod', 'tex', 'game_over_1.png')), GL_REPEAT, GL_NEAREST),
            es.toGPUShape(bs.createTextureCube(os.path.join('mod', 'tex', 'game_over_2.png')), GL_REPEAT, GL_NEAREST),
            es.toGPUShape(bs.createTextureCube(os.path.join('mod', 'tex', 'game_over_3.png')), GL_REPEAT, GL_NEAREST),
            es.toGPUShape(bs.createTextureCube(os.path.join('mod', 'tex', 'game_over_4.png')), GL_REPEAT, GL_NEAREST)
        ])
        self.x, self.y, self.z = 0, 310, 100
        self.phi = 0
        self.tick = 0
        self.s = 10
        self.transform = tr.matmul([tr.translate(self.x, self.y, self.z), tr.scale(self.s, self.s, 0.0001)])
        
    def draw(self, pipeline, projection, view):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPU[0])
    
    def update(self):
        self.GPU.append(self.GPU.popleft())
        self.tick -= 0.1 * np.exp(self.tick/10)
        self.phi = np.exp(self.tick)
        self.transform = tr.matmul([tr.translate(self.x, self.y, self.z), tr.rotationX(2 * self.phi), tr.rotationZ(self.phi),  tr.scale(self.s, self.s, 0.0001)])
