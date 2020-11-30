import os
import sys

import glfw
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr
import lib.lighting_shaders as ls
from controller.controller import Controller

from model.models import Floor, Sky, Snake

def view():
    
    if not glfw.init(): sys.exit()
        
    WIDTH = 800; HEIGHT = 800
    window = glfw.create_window(WIDTH, HEIGHT, 'BOB', None, None)
    
    if not window: glfw.terminate(); sys.exit()
        
    glfw.make_context_current(window)
    
    controller = Controller()
    glfw.set_key_callback(window, controller.on_key)
    
    floor = Floor()
    sky = Sky()
    snake = Snake(); controller.snake = snake
    
    lava = bs.createTextureCube(os.path.join('model','lava.png'))
    GPUlava = es.toGPUShape(lava, GL_REPEAT, GL_LINEAR)
    # lava_transform = tr.matmul([tr.translate(0,0,-20),tr.uniformScale(20)])
    
    pipeline = es.SimpleModelViewProjectionShaderProgram()
    texture_pipeline = es.SimpleTextureModelViewProjectionShaderProgram()
    lighting_pipeline = ls.SimplePhongShaderProgram()
    glUseProgram(pipeline.shaderProgram)
    glClearColor(0.85, 0.85, 0.85, 1.0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    projection = tr.perspective(45, float(WIDTH)/float(HEIGHT), 0.1, 100)
    view = tr.lookAt(
            #np.array([10,10,5]), # eye
            #np.array([0,0,0]), # at
            #np.array([0,0,1])  # up
            np.array([0,-40,40]), # eye
            np.array([0,0.0001,0]), # at
            np.array([0,0,1])  # up
    )
    
    while not glfw.window_should_close(window):
        
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        floor.draw(texture_pipeline,projection,view)
        sky.draw(texture_pipeline,projection,view)
        snake.move()
        snake.draw(texture_pipeline,projection,view)
        
        for x,y in [[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1]]:
            lava_transform = tr.matmul([tr.translate(x*20,y*20,-20),tr.uniformScale(20)])
            glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "model"), 1, GL_TRUE, lava_transform)
            glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            texture_pipeline.drawShape(GPUlava)
        
        glUseProgram(lighting_pipeline.shaderProgram)
        
        glfw.swap_buffers(window)
        
    glfw.terminate()
        
    
    
if __name__ == '__main__':
    view()