import os
import sys

import glfw
from OpenGL.GL import *

from data.mydata import d
import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.scene_graph as sg
import lib.transformations as tr
from model.models import Snake, Chessboard, GameOver, Apple
from controller.controller import Controller
try:
    if d["s"]:
        try:
            from lib.playsound import playsound
        except ImportError:
            d["s"] = False
            d.dump()
except KeyError:
    pass
    

def start():
    
    d.load()
    if d["s"]:
        playsound(os.path.join("data", "hola.mp3"), block=False)
    
    if not glfw.init():
        sys.exit()
        
    window = glfw.create_window(d["w"], d["h"], 'Snake', None, None)
    if not window:
        glfw.terminate()
        sys.exit
    glfw.make_context_current(window)
    
    controller = Controller()
    chessboard = Chessboard(d["n"])
    snake = Snake()
    apple = Apple()
    gameover = GameOver()
    
    controller.snake = snake
    glfw.set_key_callback(window, controller.on_key)
    
    pipeline_transform = es.SimpleTransformShaderProgram()
    pipeline_texture = es.SimpleTextureTransformShaderProgram()
                
    glClearColor(0, 0, 0, 1.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    t_last_update = 0
    t_last_frame = 0
    fps_limit = 1/d["fps"]
    
    while not glfw.window_should_close(window):
        
        t_now = glfw.get_time()
        dt = t_now - t_last_update
        
        
        glfw.poll_events()
        
        if t_now - t_last_frame >= fps_limit and snake.is_alive:
            
            glfw.set_window_title(window, f'Snake [FPS: {1/(t_now - t_last_frame):.0f}]')
            
            glClear(GL_COLOR_BUFFER_BIT)
            
            glUseProgram(pipeline_texture.shaderProgram)
            chessboard.draw(pipeline_texture)
            snake.update(apple)
            snake.draw(pipeline_texture, apple)
            glUseProgram(pipeline_transform.shaderProgram)
            apple.draw(pipeline_transform, t_now)
            
            glfw.swap_buffers(window)
            
            t_last_frame = t_now
            
        elif not snake.is_alive:

            glClear(GL_COLOR_BUFFER_BIT)

            glfw.set_window_title(window, f'Snake :(')
            glUseProgram(pipeline_texture.shaderProgram)
            gameover.update()
            gameover.draw(pipeline_texture)
            
            glfw.swap_buffers(window)
            
            if snake.r:
                glfw.terminate()
                return start()
        
        t_last_update = t_now
        
    glfw.terminate()