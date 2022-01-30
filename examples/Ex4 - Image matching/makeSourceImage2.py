# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 03:18:13 2021

@author: Christian
"""
from PIL import Image, ImageDraw
import time
import numpy as np
# from skimage.metrics import structural_similarity as ss


from functions import renderImg

dx = 200
dy = 200



targetImg = Image.new('RGB', (dx, dy), (255, 255, 255))
draw = ImageDraw.Draw(targetImg, "RGBA")
draw.ellipse((50, 50, 150, 150), fill=(0, 0, 0, 255))
pixelsTarget = np.array(targetImg)


t1 = time.time()
# img = Image.new('RGBA', (dx, dy), (0, 0, 0, 255))
img = Image.new('RGB', (dx, dy), (255, 255, 255))
draw = ImageDraw.Draw(img, "RGBA")
Ncircle = 1000
lims = np.array([dx, dy, 10, 255])


# img.save('white.jpg')
np.random.seed(40)
limits = np.random.uniform(0, 1,[Ncircle,4]) * lims
# limits = np.array(np.rint(limits), dtype=int)

x1 = limits[:,0] - limits[:,2]
x2 = limits[:,0] + limits[:,2]
y1 = limits[:,1] - limits[:,2]
y2 = limits[:,1] + limits[:,2]

points = np.column_stack([x1,y1,x2,y2,limits[:,-1]])

for val in points:
    draw.ellipse(tuple(val[:-1]), fill=(0, 0, 0, int(val[-1])) )
    # draw.ellipse(tuple(val[:-1]), fill=(0, 0, 0, 0) )
# draw.ellipse((10, 10, 40, 100), fill=(0, 0, 0, 100))


t2 = time.time()
# img.show()

pixelsImage = np.array(img)


diff = np.sum((pixelsImage - pixelsTarget)**2)
# diff2 = ss(pixelsImage, pixelsTarget,multichannel=True)

diff = np.sum((pixelsImage - pixelsTarget)**2)

print(t2 - t1)
print(diff)

# print(img)
# img = renderImg(limits[:,0],limits[:,1],limits[:,2],limits[:,3], dx, dy)
