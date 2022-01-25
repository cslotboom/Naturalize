# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 23:57:18 2021

@author: Christian
"""

from PIL import Image, ImageDraw
# import time
import numpy as np

# from skimage.metrics import structural_similarity as ss


class Environment:
    
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


def testIndividual(individual, dx, dy):
    """
    Tests and individual and returns the result of that test.
    
    The user should consider if it's possible for the test not to work.
    
    """
    
    [x0, y0, r, alpha] = individual.genotype
    img =  renderImg(x0, y0, r, alpha, dx, dy)
    pixels = np.array(img, float)
    return img, pixels

def ftest(individual, env):
    """
    """
    
    result = testIndividual(individual, env.dx, env.dy)
    return result[1]

def fitness(individual, environment):
    # Npoint = len(route)
    # Indexes = np.arange(Npoint)
    
    imgPixel = individual.result[1]
    targetPixels = environment.targetPixels
    
    diff = np.sum((imgPixel - targetPixels)**2)
    
    return diff

def renderImg(x0, y0, r, alpha, dx, dy):

    # gene = [x0, y0, r, alpha]
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
    