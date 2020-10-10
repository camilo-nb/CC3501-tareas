import sys
import glfw
from src.models.actor.snake import Snake

class Controller():
    
    def __init__(self):
        self.__snake = None
    
    @property
    def snake(self):
        return self.__snake
    
    @snake.setter
    def snake(self, value):
        assert isinstance(value, Snake)
        self.__snake = value
    
    def on_key(self, window, key, scancode, action, mods):
        
        if not action == glfw.PRESS or action == glfw.RELEASE:
            return

        if key == glfw.KEY_ESCAPE:
            sys.exit()


        elif (key == glfw.KEY_UP or key == glfw.KEY_W) and action == glfw.PRESS:
            self.__snake.new_mov = "w"
            
        elif (key == glfw.KEY_LEFT or key == glfw.KEY_A) and action == glfw.PRESS:
            self.__snake.new_mov = "a"
            
        elif (key == glfw.KEY_DOWN or key == glfw.KEY_S) and action == glfw.PRESS:
            self.__snake.new_mov = "s"
            
        elif (key == glfw.KEY_RIGHT or key == glfw.KEY_D) and action == glfw.PRESS:
            self.__snake.new_mov = "d"