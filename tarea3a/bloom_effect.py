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
R : 8-bit unsigned integer
    Light red channel value.
G : 8-bit unsigned integer
    Light green channel value.
B : 8-bit unsigned integer
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
from scipy.sparse import dok_matrix
from scipy.sparse.linalg import spsolve

__author__ = "Camilo Núñez Barra"
print(sys.argv)
# Handling input
if len(sys.argv) != 6: raise Exception("Invalid length of arguments. Follow:\n$ python bloom_effect.py image_filename N R G B")
im_filename = sys.argv[1]
r = int(sys.argv[2])
color = np.array(sys.argv[3:6], dtype=np.uint8)

im = Image.open(im_filename)
rgb = np.array(im.convert("RGB"), dtype=np.uint8) # RGB 0..255
rgb_ = rgb.astype(float)/255 # RGB 0..1

# Target (Dirichlet boundary conditions)
light = np.logical_and.reduce((rgb == color), axis=2, dtype=np.uint8)
ij2k = {}; k = 0 # Bijection: coordinates (i,j) <-> label k (unknowns)

nx, ny = light.shape
for i, j in np.ndindex(nx,ny):
    y, x = np.ogrid[-i:nx-i,-j:ny-j] # Axes of blur disk centered on each pixel
    disk = x*x + y*y <= r*r # Blur disk mask within range
    # >0 if pixel within range. =0 if not && Check if it's light or pixel to blur
    if light[disk].sum() and np.maximum(1-light[i][j], 0): ij2k[(i,j)] = (k:=k+1)

# Light follows Laplace's equation, discretized using finite
# difference method. Solve A*x=b in order find the unknowns.
A = np.empty(3, dtype=object) # Coefficient of the unknowns
b = np.zeros((k,3), dtype=float) # Right side (Dirichlet boundary conditions)
for i in range(3): A[i] = dok_matrix((k,k), dtype=float) # Sparse matrix

for (i,j), k in ij2k.items():

    # Five-point stencil
    ku = ij2k.get((i,j+1)) # up
    kd = ij2k.get((i,j-1)) # down
    kl = ij2k.get((i-1,j)) # left
    kr = ij2k.get((i+1,j)) # right

    # Three cases:
    # light=0 (no light -> no contribution)
    # light=1 (light -> Dirichlet)
    # i or j index out of range (neither -> no contribution)
    try: bu = light[i][j+1] * rgb_[i][j+1]
    except IndexError: bu = np.zeros(3, dtype=float)
    try: bd = light[i][j-1] * rgb_[i][j-1]
    except IndexError: bd = np.zeros(3, dtype=float)
    try: bl = light[i-1][j] * rgb_[i-1][j]
    except IndexError: bl = np.zeros(3, dtype=float)
    try: br = light[i+1][j] * rgb_[i+1][j]
    except IndexError: br = np.zeros(3, dtype=float)

    # k_ is None if it is not an unknown
    if ku: A[0][k-1,ku-1], A[1][k-1,ku-1], A[2][k-1,ku-1] = np.ones(3, dtype=float)
    if kd: A[0][k-1,kd-1], A[1][k-1,kd-1], A[2][k-1,kd-1] = np.ones(3, dtype=float)
    if kl: A[0][k-1,kl-1], A[1][k-1,kl-1], A[2][k-1,kl-1] = np.ones(3, dtype=float)
    if kr: A[0][k-1,kr-1], A[1][k-1,kr-1], A[2][k-1,kr-1] = np.ones(3, dtype=float)
    A[0][k-1, k-1], A[1][k-1, k-1], A[2][k-1, k-1] = -4*np.ones(3, dtype=float)
    b[k-1] = -bu-bd-bl-br

x = np.empty((A.shape[0], A[0].shape[0]))
for i in np.arange(A.shape[0]): x[i] = spsolve(A[i].tocsr(), b.transpose()[i])

# Add up light -> blur disks
for (i,j), k in ij2k.items(): rgb_[i][j] += x.T[k-1]
rgb = (np.clip(rgb_,0,1)*255.999).astype(np.uint8) # RGB 0..1 to 0..255

fn, e = os.path.splitext(im_filename)
im_out = Image.fromarray(rgb)
if im.mode == "RGBA": im_out.putalpha(im.split()[-1])
im_out.save(fn+"_out"+e)
