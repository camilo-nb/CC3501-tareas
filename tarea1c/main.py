#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""main.py

blah blah blah description docstring
"""
                                                                              # 79 characters limit
import glfw                                                                   # all lines
import OpenGL.GL                                                              #
import OpenGL.GL.shaders                                                      #
                                                                              #
import numpy as np                                                            #
                                                                              #
__author__ = "Camilo Núñez Barra"                                             #
__version__ = "a0.0.0"                                                        #
__date__ = "2020-09-22 22:30:00"                                              #
__email__ = "camilo.nunez@ug.uchile.cl"                                       #
__license__ = "MIT"                                                           #
__status__ = "Prototype"                                                      #
                                                                              #
def function(argument, x, a = 'a'):                                           #
    """Short summary.                                                  # 72 characters limit
                                                                       # docstrings or comments
    Extended Summary...                                                #
                                                                       #
    ...continues.                                                      #
                                                                       #
    Parameters                                                         #
    ----------                                                         #
    argument : type                                                    #
        Description of parameter `argument`.                           #
    x                                                                  #
        Description of parameter `x` (with type not specified).        #
    a : str, optional                                                  #
        Description of parameter `a` (the default is 'a',              #
        which is the first letter of the alphabet).                    #
                                                                       #
    Returns                                                            #
    -------                                                            #
    int                                                                #
        Description of anonymous integer return value.                 #
                                                                       #
    Raises                                                             #
    ------                                                             #
    LinAlgException                                                    #
        If the matrix is not numerically invertible.                   #
                                                                       #
    """
    
    if a == 'b':
        raise ValueError
    
    return 0
        
class Photo(list):
    """
    List with associated photographic information.

    ...

    Attributes
    ----------
    exposure : float
        Exposure in seconds.

    Methods
    -------
    colorspace(c='rgb')
        Represent the photo in the given colorspace.
    gamma(n=1.0)
        Change the photo's gamma exposure.

    """
    
    pass


if __name__ == "__main__":
    pass
