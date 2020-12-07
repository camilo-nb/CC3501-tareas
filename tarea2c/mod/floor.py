import os

from OpenGL.GL import *

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr

class Floor():
    def __init__(self):
        self.GPU = es.toGPUShape(bs.createTextureCube(os.path.join('mod','tex','floor.png')), GL_REPEAT, GL_LINEAR)
        self.s = 100
        self.x,self.y, self.z = 0, 0, -self.s/2
        self.transform = tr.matmul([tr.translate(self.x,self.y,self.z),tr.uniformScale(self.s)])
    def draw(self, pipeline, projection, view):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPU)
        