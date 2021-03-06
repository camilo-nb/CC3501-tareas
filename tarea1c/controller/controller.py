import os
import sys

import glfw

class Controller():
    
    def __init__(self):
        
        self.snake = None
        
    def on_key(self, window, key, scancode, action, mods):
        if not (action == glfw.PRESS or action == glfw.RELEASE):
            return

        if key == glfw.KEY_ESCAPE:
            glfw.terminate()
            sys.exit()
        
        if self.snake.is_alive:
            if (key == glfw.KEY_W or key == glfw.KEY_UP) and action == glfw.PRESS:
                if self.snake.dy != -1:
                    self.snake.dx, self.snake.dy = 0, 1
            
            elif (key == glfw.KEY_S or key == glfw.KEY_DOWN) and action == glfw.PRESS:
                if self.snake.dy != 1:
                    self.snake.dx, self.snake.dy = 0, -1
                
            elif (key == glfw.KEY_A or key == glfw.KEY_LEFT) and action == glfw.PRESS:
                if self.snake.dx != 1:
                    self.snake.dx, self.snake.dy = -1, 0
                
            elif (key == glfw.KEY_D or key == glfw.KEY_RIGHT) and action == glfw.PRESS:
                if self.snake.dx != -1:
                    self.snake.dx, self.snake.dy = 1, 0
                
        else:
            if key == glfw.KEY_F and action == glfw.PRESS:
                if not self.snake.f:
                    self.snake.f = True
            
            elif key == glfw.KEY_R and action == glfw.PRESS:
                if not self.snake.f:
                    self.snake.r = True