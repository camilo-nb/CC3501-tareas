import sys

import glfw

class Controller():
    def __init__(self): self.snake=None
    def on_key(self, window, key, scancode, action, mods):
        if not (action == glfw.REPEAT or action == glfw.PRESS or action == glfw.RELEASE): return

        if key == glfw.KEY_ESCAPE: glfw.terminate(); sys.exit()
        
        if (key == glfw.KEY_W or key == glfw.KEY_UP) and (action == glfw.PRESS or action == glfw.REPEAT):
            pass
        elif (key == glfw.KEY_S or key == glfw.KEY_DOWN) and (action == glfw.PRESS or action == glfw.REPEAT):
            pass
        elif (key == glfw.KEY_A or key == glfw.KEY_LEFT) and (action == glfw.PRESS or action == glfw.REPEAT):
            self.snake.turn_left()
        elif (key == glfw.KEY_D or key == glfw.KEY_RIGHT) and (action == glfw.PRESS or action == glfw.REPEAT):
            self.snake.turn_right()