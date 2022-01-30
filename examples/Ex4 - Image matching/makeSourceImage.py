# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 01:53:59 2021

@author: Christian
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

from PIL import Image, ImageDraw


x1 = 50
x2 = 610
y1 = 110
y2 = 520

output_image_path = 'naturalize_bw.jpg'
img = Image.open('naturalize.jpg')
img = img.crop(box=(x1,y1,x2,y2))

dx = int((x2 - x1)/2)
dy = int((y2 - y1)/2)
bw = img.convert('L')
bw = bw.resize((dx, dy))

# bw.show()
bw.save(output_image_path)