# -*- coding: utf-8 -*-
"""
@author: CS
Make a gif of the results

"""


import matplotlib.pyplot as plt
import numpy as np
import naturalize as nat
import imageio
from functions import plotIndividual, environment


"""
Initialize the environment. This is done because some of the data used by
plot Individual is stored in the environmen.
"""
xlims = np.array([0,2])
ylims = np.array([0,2])
trussMat = 10       # can be 10 or 11
forces = np.array([5000., 5000., 0.])
env = environment(xlims, ylims, trussMat, forces)

"""
Read the input data.
"""

dataName = 'Analysis data.P'
data = nat.readPickle(dataName) 

# Save images
images = []
fileNames = []
for ii, genotype in enumerate(data.bestIndividuals):
    fig, ax = plotIndividual(genotype, env)
    gen = (ii+1)*5
    plt.text(1.7, 2.8, f'Gen. {gen}', {'color':  'white','size': 16} )
    
    filename = f'img/gen_{ii}.png'
    plt.savefig(filename)
    fileNames.append(filename)
    plt.close()


"""
Make the output gif
"""    
with imageio.get_writer('mygif.gif', mode='I') as writer:
    for filename in fileNames:
        image = imageio.imread(filename)
        writer.append_data(image)    
    






