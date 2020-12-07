import numpy as np

import lib.transformations as tr

class Camera():
    
    def __init__(self):
        self.snake = None
        self.camera = 0 # 0:my_view, 1:top_view, 2:diagonal_view

    @property
    def view(self):
        if self.camera == 0:
            return tr.lookAt(
                np.array([self.snake.x + np.cos(self.snake.phi) * -10, self.snake.y + np.sin(self.snake.phi) * -10, 5]),
                np.array([self.snake.x + np.cos(self.snake.phi)      , self.snake.y + np.sin(self.snake.phi)      , 0]),
                np.array([0                                          , 0                                          , 1])
            )
        elif self.camera == 1: return tr.lookAt(np.array([0, 0, 50]), np.array([0, 0.1, 0]), np.array([0, 0, 1]))
        elif self.camera == 2: return tr.lookAt(np.array([0, -50, 50]), np.array([0, 0.1, 0]), np.array([0, 0, 1]))
        
    def snake_view(self): self.camera = 0
    def top_view(self): self.camera = 1
    def diagonal_view(self): self.camera = 2