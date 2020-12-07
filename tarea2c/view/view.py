import sys

import glfw
from OpenGL.GL import *

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr
import lib.lighting_shaders as ls

from view.camera import Camera
from ctr.controller import Controller
from mod.models import Snake, Floor

def view():
    
    if not glfw.init(): sys.exit()
    
    WIDTH = 800; HEIGHT = 800
    window = glfw.create_window(WIDTH, HEIGHT, 'SNAKE 3D', None, None)
    if not window: glfw.terminate(); sys.exit()
    glfw.make_context_current(window)
    
    controller = Controller(); glfw.set_key_callback(window, controller.on_key)
    camera = Camera(); controller.camera = camera
    snake = Snake(); controller.snake = snake; camera.snake = snake
    floor = Floor()
    
    texture_pipeline = es.SimpleTextureModelViewProjectionShaderProgram()
    lighting_pipeline = ls.SimpleTexturePhongShaderProgram()
    projection = tr.perspective(45, float(WIDTH)/float(HEIGHT), 0.1, 100)
    glClearColor(0.85, 0.85, 0.85, 1.0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    FPS_LIMIT = 1.0 / 30.0
    frames = 0
    updates = 0 
    timer = 0
    time_last = 0
    time_delta = 0
    time_now = 0
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        time_now = glfw.get_time()
        time_delta += (time_now - time_last) / FPS_LIMIT
        time_last = time_now

        while time_delta >= 1.0:
            snake.update()
            updates += 1
            time_delta -= 1.0
        #snake.update()
        view = camera.view
        snake.draw(lighting_pipeline, projection, view)
        floor.draw(texture_pipeline, projection, view)
        
        frames += 1
        glfw.swap_buffers(window)
        
        if glfw.get_time() - timer > 1.0:
            timer += 1
            print(f"FPS: {frames} Updates: {updates}")
            updates = 0
            frames = 0
        
    glfw.terminate()