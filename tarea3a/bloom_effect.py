#!/usr/bin/python
# -*- coding: utf-8 -*-

"""bloom_effect.py

The effect produces fringes (or feathers) of light
extending from the borders of bright areas in an image,
contributing to the illusion of an extremely bright light
overwhelming the camera or eye capturing the scene. [1]

Run
---
$ python bloom_effect.py image_filename N R G B

Parameters
----------
image_filename : string
    Name of the image file to be applied the effect.
N : unsigned integer
    Light blur disk radius (effect range).
R : 8-bit integer
    Light red channel value.
G : 8-bit integer
    Light green channel value.
B : 8-bit integer
    Light blue channel value.

Returns
-------
image_filename_out : file
    Image file with effect applied.

Notes
-----
The RGB value should be chosen wisely. This script blurs
that exact value without considering a range of colors.
This effect expects an RGB value of light to obtain
a well blurred result, otherwise it won't blur as expected,
because it lights up the disk but not the RGB value itself.

References
----------
.. [1] https://en.wikipedia.org/wiki/Bloom_(shader_effect)
"""

import os
import sys

import numpy as np
from PIL import Image

__author__ = "Camilo Núñez Barra"

# Handling input
if len(sys.argv) != 6: raise Exception("Invalid length of arguments. Follow:\n$ python bloom_effect.py image_filename N R G B")
im_filename = sys.argv[1]
r = int(sys.argv[2])
color = np.array(sys.argv[3:6], dtype=np.uint8)

im = Image.open(im_filename)
rgb = np.array(im.convert('RGB'), dtype=np.uint8) # RGB 0..255
rgb_ = rgb.astype(float)/255 # RGB 0..1
if im.mode == 'RGBA': alpha = im.split()[-1]

target = np.logical_and.reduce((rgb == color), axis=2, dtype=np.uint8) # Light (Dirichlet boundary conditions)
unknown = np.zeros_like(target) # Pixels to blur
k2ij, ij2k = {}, {}; k = 0 # Bijection: coordinates (i,j) <-> label k (for pixels unknown)

nx, ny = target.shape
for i, j in np.ndindex(nx,ny):
    
    y, x = np.ogrid[-i:nx-i,-j:ny-j] # Axes of blur disk centered on each pixel
    mask = x*x + y*y <= r*r # Blur disk mask within range
    if target[mask].sum(): # Positive if pixel within blur range. Zero if not.
        
        unknown[i][j] = np.maximum(1-target[i][j], 0) # Check if it's light or pixel to blur
        if unknown[i][j]:
            k+=1
            k2ij[k] = (i,j)
            ij2k[(i,j)] = k

# Light follows Laplace's equation, discretized using finite
# difference method. Solve A*x=b in order find the unknowns.
A = np.zeros((k,k,3), dtype=float) # Coefficient of the unknowns
b = np.zeros((k,3), dtype=float) # Right side (Dirichlet boundary conditions)

for k, (i,j) in k2ij.items():

    # Five-point stencil
    ku = ij2k.get((i,j+1)) # up
    kd = ij2k.get((i,j-1)) # down
    kl = ij2k.get((i-1,j)) # left
    kr = ij2k.get((i+1,j)) # right

    # Three cases:
    # target=0 (no light -> no contribution)
    # target=1 (light -> Dirichlet)
    # i or j index out of range (neither -> no contribution)
    try: bu = target[i][j+1] * rgb_[i][j+1]
    except IndexError: bu = np.zeros(3)
    try: bd = target[i][j-1] * rgb_[i][j-1]
    except IndexError: bd = np.zeros(3)
    try: bl = target[i-1][j] * rgb_[i-1][j]
    except IndexError: bl = np.zeros(3)
    try: br = target[i+1][j] * rgb_[i+1][j]
    except IndexError: br = np.zeros(3)

    # k_ is None if it is not an unknown
    if ku: A[k-1,ku-1] = np.ones(3)
    if kd: A[k-1,kd-1] = np.ones(3)
    if kl: A[k-1,kl-1] = np.ones(3)
    if kr: A[k-1,kr-1] = np.ones(3)
    A[k-1, k-1] = -4*np.ones(3)
    b[k-1] = -bu-bd-bl-br

# C'mon NumPy, hurry up!
x = np.linalg.solve(A.T, b.T)

# Add up light -> blur disks
for k, (i,j) in k2ij.items(): rgb_[i][j] += x.T[k-1]
np.clip(rgb_,0,1,out=rgb_)
rgb = (rgb_*255.999).astype(np.uint8)

fn, e = os.path.splitext(im_filename)
im_out = Image.fromarray(rgb)
if im.mode == 'RGBA': im_out.putalpha(alpha)
im_out.save(fn+'_out'+e)
