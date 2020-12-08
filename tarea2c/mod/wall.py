import os

import numpy as np
from OpenGL.GL import *

import lib.easy_shaders as es
import lib.object_handler as oh
import lib.transformations as tr


class Wall():
    def __init__(self):
        self.GPU = es.toGPUShape(oh.readOBJ2(os.path.join('mod','tex','wall.obj'), os.path.join('mod','tex','wall.png')), GL_REPEAT, GL_NEAREST)
        self.s = 200
        self.x,self.y, self.z = 0, 0, self.s-6
        self.transform = np.matmul(tr.translate(self.x,self.y,self.z),tr.uniformScale(self.s))
    def draw(self, pipeline, projection, view, food):
        if food.status == 'pikachu': light_pos = [food.x, food.y, food.z]; shininess = 10000
        else: light_pos = [50, 50,50]; shininess = 10000
        glUseProgram(pipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), *light_pos)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), self.x, self.y ,self.z)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), shininess)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.1)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.1)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.1)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPU)
        