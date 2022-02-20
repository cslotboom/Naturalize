# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 16:53:36 2022

@author: Christian
"""

# # from sys import path
import matplotlib.pyplot as plt
import numpy as np
# import pathlib 
# import sys
  
# # directory reach
# directory = pathlib.path(__file__).abspath()
  
# # setting path
# sys.path.append(directory.parent.parent)
from functions import plotIndividual

areas = [37.19293627, 97.62828497, 98.41511705, 98.67276891, 99.4588365,  99.98164484,
         98.98731974, 97.39164825, 89.23520808, 99.27441342, 99.94593253]
areas = np.array([4.72681207e-07, 4.62150712e-05, 9.30654961e-05, 6.29463882e-05,
                   3.19021097e-05, 4.49502543e-05, 3.01790297e-05, 6.40384157e-05,
                   3.58360447e-05, 4.47831852e-05, 3.01350333e-05])
maxArea = max(areas)


fig, ax = plotIndividual(areas)
fig.set_figwidth(2)
fig.set_figheight(6)
# plt.rc('font', size=15) 
# fig.show()

for text in ax.texts:
    text.set_fontsize(10)

ax.texts = []
    
for ii, line in enumerate(ax.lines):
    line.set_linewidth(5*areas[ii]/maxArea)
    
fig.savefig("mygraph.png")