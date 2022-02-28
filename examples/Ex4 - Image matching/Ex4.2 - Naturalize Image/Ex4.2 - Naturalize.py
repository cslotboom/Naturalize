# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 00:30:05 2021

@author: Christian

In this example, an image is drawn of with a series of 2500 circles

Atwork is taken from the 2002 printing of the "Naturalize"
Magic the Gathering card by Wizards of the coast.
Original illustration by Ron Spears.

See the functions file for for a detailed explanation of imported functions.

"""

import naturalize as nat
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('..')
from functions import Environment, ftest, fitness, renderImg

"""
Define the analysis and outputs for the analysis.
Note, this analysis would take a very long time to complete. It's recommended
that the analysis is run in iteratiions of generations with a size of 50k.
This can be acomplisehed by saving outputs of an old generation and using it 
as an input for the initial generation of the next analysis.
"""
outputGen = 'Gen800000.P'
Ngen = 800000
outputData= '800k.P'
gifName = 'Naturalize.gif'

"""
Load in the target data and set the envirionment to the correct image.
"""
dx = 252
dy = 204
ImageName = 'Ex4.2-target.jpg'
env = Environment(dx,dy, ImageName)

"""
Next a basic gene pool is defined for the problem. Four genes are used:
    [xposition, yposition, radius, opacity]
Each gene is a vector with a value for each circle
"""
Ncircle = 2500
rmin = 1
rmax = 10
lims = np.array([dx, dy, rmax, 255])
llims =  [np.zeros(Ncircle), np.zeros(Ncircle), np.ones(Ncircle)*rmin, np.zeros(Ncircle) * 0.]
ulims =  [np.ones(Ncircle)*dx, np.ones(Ncircle)*dy, np.ones(Ncircle)*rmax, np.ones(Ncircle)*255]

genePool = nat.BasicGenePool(llims, ulims)
fmut = nat.getMutate(0)
helper = nat.AlgorithmHelper(ftest,  genePool, fitness, fmut, environment = env)

"""
Next the number of individuals, couples, and survivers in the analysis is 
chosen. A small gene pool, with many couples and one surviver is used to ensure
that progress is made on the best solution. A moderate mutation rate is used, 
because the solution space is so big. A good rule of thumb is 1/N.

There are no hard rules for selecting these parameters, and other values
would be appripriate. Consider playing around the parameters to see how they 
affect the analysis.
"""
Npop = 10
Ncouples = 4
Nsurvive = 1
mutateThresold = 0.0001

algorithm = nat.GeneticAlgorithm(helper, Npop, Ncouples, Nsurvive,  mutateThresold)
recorder = nat.basicRecorder(100, 1)
analysis = nat.Analysis(algorithm, recorder)

best = analysis.runAnalysis(Ngen)
data = analysis.getRecorderData()

"""
Save both teh current generations, and the output data.
The current generation can be used as a checkpoint to restart the analysis.
"""
nat.pickleData(data, outputData)
nat.pickleData(analysis.currentGen, outputGen)

"""
Plot an image of hte function to see how well it did
"""
plt.plot(data.genNumber, data.bestScores)
img = renderImg(*best, dx,dy)

"""
Plot the analyiss over time, and the score of one gene
"""
nat.plotAvgScore(data)
nat.plotGeneValue(data, 2, 1)

"""
Create a gif of teh ouput image.
"""
images = []
for genotype in data.bestGenotypes:
    img = renderImg(*genotype, dx,dy)
    images.append(img)
    
images[0].save(gifName,
               save_all = True, append_images = images[1:], 
               optimize = False, duration = 2)

