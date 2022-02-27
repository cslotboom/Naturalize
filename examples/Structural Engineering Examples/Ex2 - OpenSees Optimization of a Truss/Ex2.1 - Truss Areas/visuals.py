# -*- coding: utf-8 -*-
"""
@author: CS
Make a gif of the results

"""


import matplotlib.pyplot as plt
import numpy as np
import naturalize as nat
import imageio
from functions import plotIndividual

inputData = 'Normalized analysis data.P'
data = nat.readPickle(inputData) 

# Save images
images = []
fileNames = []
for ii, genotype in enumerate(data.bestGenotypes):
    fig, ax = plotIndividual(genotype[0])
    plt.text(1.7, 2.8, f'Gen. {(ii+1)*5}', {'color':  'white','size': 16} )
    
    filename = f'img/gen_{ii}.png'
    plt.savefig(filename)
    fileNames.append(filename)
    plt.close()
  
    
# Make the output gif
with imageio.get_writer('mygif.gif', mode='I') as writer:
    for filename in fileNames:
        image = imageio.imread(filename)
        writer.append_data(image)    
    






