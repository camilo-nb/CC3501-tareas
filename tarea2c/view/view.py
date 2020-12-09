import sys
import time

import glfw
from OpenGL.GL import *

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr
import lib.lighting_shaders as ls

from view.camera import Camera
from ctr.controller import Controller
from mod.models import Snake, Floor, Food, Wall, Water, GameOver, Obstacle

def start():
    
    if not glfw.init(): sys.exit()
    
    WIDTH = 1000; HEIGHT = 1000
    window = glfw.create_window(WIDTH, HEIGHT, 'SNAKE 3D', None, None)
    if not window: glfw.terminate(); sys.exit()
    glfw.make_context_current(window)
    
    controller = Controller(); glfw.set_key_callback(window, controller.on_key)
    camera = Camera(); camera.w = WIDTH; camera.h = HEIGHT; controller.camera = camera
    snake = Snake(); controller.snake = snake; camera.snake = snake
    floor = Floor()
    food = Food()
    wall = Wall()
    water = Water()
    game_over = GameOver()
    obstacle = Obstacle()
    
    texture_pipeline = es.SimpleTextureModelViewProjectionShaderProgram()
    lighting_pipeline = ls.SimplePhongShaderProgram()
    lighting_texture_pipeline = ls.SimpleTexturePhongShaderProgram()
    glClearColor(0.0, 0.0, 0.0, 1.0)
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
            if snake.alive:
                snake.update(food, obstacle)
                food.update()
            else:
                game_over.update()
            updates += 1
            time_delta -= 1.0
        if snake.alive:
            projection, view = camera.projection, camera.view
            snake.draw(lighting_texture_pipeline, projection, view, food)
        else:
            camera.game_over_view()
            projection, view = camera.projection, camera.view
            game_over.draw(texture_pipeline, projection, view)
            if controller.restart: break
        
        obstacle.draw(lighting_texture_pipeline, projection, view, food)
        floor.draw(lighting_texture_pipeline, projection, view, food)
        wall.draw(lighting_texture_pipeline, projection, view, food)
        water.draw(lighting_texture_pipeline, projection, view, food)
        food.draw(lighting_pipeline, projection, view)
            
        frames += 1
        glfw.swap_buffers(window)
        
        if glfw.get_time() - timer > 1.0:
            timer += 1
            print(f"FPS: {frames} Updates: {updates}")
            updates = 0
            frames = 0
        
    glfw.terminate()
    if controller.restart: start()
