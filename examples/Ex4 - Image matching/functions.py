# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 23:57:18 2021

Funcitons that are used to compare images with the base image. The PIL package
is used to generate the images in the model.
"""

from PIL import Image, ImageDraw
import numpy as np

class Environment:
    """
    First we'll create the environment. In this case, it just contains 
    information about the canvas size, and the target image we want to match.
    The dx data must match the target imgage in this case.
    """
    
    
    def __init__(self, dx, dy, imageName):
        self.dx = dx
        self.dy = dy
        self.setTargetImg(imageName)
        
    def setTargetImg(self, imageName):
        
        targetImg = Image.open(imageName)
        targetImg = targetImg.convert('RGB')
        pixelsTarget = np.array(targetImg, float)
        
        self.target = targetImg
        self.targetPixels = pixelsTarget

"""
This is the function used to render each image, based on it's gene pool.
The first four variables are defined by each gene, while dx and dy are fixed 
and will come from the envirionment.
"""

def renderImg(x0, y0, r, alpha, dx, dy):
    """
    Parameters
    ----------
    x0 : np.array
        The vector of x positions for each array.
    y0 : np.array
        The vector of y positions for each array.
    r : np.array
        The vector of radii for each array.
    alpha : np.array
        The vector, given from 1 to 255.
    dx : float
        The number of pixels in the x direction.
    dy : float
        The number of pixels in the y direction.

    Returns
    -------
    img : img
        The output image.

    """

    x1 = x0 - r
    x2 = x0 + r
    y1 = y0 - r
    y2 = y0 + r
    
    points = np.column_stack([x1, y1, x2, y2, alpha])

    img = Image.new('RGB', (dx, dy), (255, 255, 255))
    draw = ImageDraw.Draw(img, "RGBA")
    for val in points:
        draw.ellipse(tuple(val[:-1]), fill=(0, 0, 0, int(val[-1])) )
        
    return img



"""
The test funciton converts data from it's genotype form, the passes it into the 
more general 'renderImg' function and returns the resulting image

"""
# def testIndividual(individual, dx, dy):

#     """
#     Creates a rendering based on the individual
#     """
#     [x0, y0, r, alpha] = individual.genotype
#     img =  renderImg(x0, y0, r, alpha, dx, dy)
#     pixels = np.array(img, float)
#     return img, pixels

def ftest(individual, env):
    
    [x0, y0, r, alpha] = individual.genotype
    img =  renderImg(x0, y0, r, alpha, env.dx, env.dy)
    
    return img

"""
We then compare the newly created image to the target image by checking
how similar the pixels are in each image, looking at each image chanel.

A large difference means the images are dissimilar, a small one means they are
similar.
"""


def fitness(individual, environment):
    
    img = individual.result
    imgPixel = np.array(img, float)    
    targetPixels = environment.targetPixels
    
    diff = np.sum((imgPixel - targetPixels)**2)
    return diff

    