import sys

import glfw
import numpy as np

import lib.transformations as tr

class Controller():
    
    def __init__(self):
        self.snake = None
        self.camera = None
        self.restart = False
        
    def on_key(self, window, key, scancode, action, mods):
        if not (action == glfw.REPEAT or action == glfw.PRESS or action == glfw.RELEASE): return

        if key == glfw.KEY_ESCAPE: glfw.terminate(); sys.exit()
        
        if action == glfw.PRESS and (key == glfw.KEY_A or key == glfw.KEY_LEFT):
            self.snake.turn_left()
        elif action == glfw.PRESS and (key == glfw.KEY_D or key == glfw.KEY_RIGHT):
            self.snake.turn_right()
        elif action == glfw.RELEASE and (key == glfw.KEY_A or key == glfw.KEY_LEFT or key == glfw.KEY_D or key == glfw.KEY_RIGHT):
            self.snake.turn_straight()
            
        elif (key == glfw.KEY_W or key == glfw.KEY_UP) and (action == glfw.PRESS or action == glfw.REPEAT):
            pass
        elif (key == glfw.KEY_S or key == glfw.KEY_DOWN) and (action == glfw.PRESS or action == glfw.REPEAT):
            pass
        
        if key == glfw.KEY_R and action == glfw.PRESS: self.camera.snake_view()
        elif key == glfw.KEY_E and action == glfw.PRESS: self.camera.top_view()
        elif key == glfw.KEY_T and action == glfw.PRESS: self.camera.diagonal_view()
        
        if not self.snake.alive:
            if key == glfw.KEY_ENTER and action == glfw.PRESS:
                self.restart = True