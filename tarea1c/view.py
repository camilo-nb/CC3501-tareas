import os
import sys
import json

import glfw
from OpenGL.GL import *
import lib.easy_shaders as es

from src.models.actor.snake import Snake

from data.data import data

from controller import Controller

def view():
    
    if not glfw.init():
        sys.exit()
        
    window = glfw.create_window(data["width"], data["height"], 'OpenGL', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    
    controller = Controller()
    glfw.set_key_callback(window, controller.on_key)
    
    pipeline = es.SimpleTextureTransformShaderProgram()
    glUseProgram(pipeline.shaderProgram)

    glClearColor(1.0, 0.0, 1.0, 1.0)
    
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    snake = Snake()
    controller.snake = snake
    
    ti = glfw.get_time()
    t0 = ti
    _fps = 0
        
    while not glfw.window_should_close(window):

        tf = glfw.get_time()
        if tf - t0 > 1.0:
            fps = _fps
            _fps = 0
            t0 = tf
        _fps += 1
        dt = tf - ti
        ti = tf
        
        glfw.poll_events()
        
        glClear(GL_COLOR_BUFFER_BIT)
        
        snake.update(dt)
        
        snake.draw(pipeline)
        
        glfw.swap_buffers(window)
    
    glfw.terminate()
    
view()