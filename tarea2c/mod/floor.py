import os

import numpy as np
from OpenGL.GL import *

import lib.easy_shaders as es
import lib.object_handler as oh
import lib.transformations as tr


class Floor():
    def __init__(self):
        self.GPU = es.toGPUShape(oh.readOBJ2(os.path.join('mod','tex','ground.obj'), os.path.join('mod','tex','ground.png')), GL_REPEAT, GL_NEAREST)
        self.s = 100
        self.x,self.y, self.z = 0, 0, -self.s
        self.transform = np.matmul(tr.translate(self.x,self.y,self.z),tr.uniformScale(self.s))
    def draw(self, pipeline, projection, view, food):
        if food.status == 'pikachu':
            glUseProgram(pipeline.shaderProgram)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 0.9, 0.9, 0.9)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.2, 0.2, 0.2)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 1.0, 1.0, 1.0)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.2, 0.2, 0.2)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), food.x, food.y, food.z)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), self.x, self.y ,self.z)
            glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 1)
            glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.1)
            glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.000001)
            glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0000001)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            pipeline.drawShape(self.GPU)
        else:
            glUseProgram(pipeline.shaderProgram)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 0.9, 0.9, 0.9)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.2, 0.2, 0.2)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 1.0, 1.0, 1.0)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.2, 0.2, 0.2)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 0, 0, 50)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), self.x, self.y ,self.z)
            glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 10000)
            glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.0001)
            glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
            glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.001)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            pipeline.drawShape(self.GPU)
        