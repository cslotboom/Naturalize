# -*- coding: utf-8 -*-
"""
@author: CS

Genetic optimization can be used to solve a number of complex problem.
In this example, the position, radius, and opacity of circles on a grid are 
chosen to match a target image - in this case just a circle in the middle of
a small 200x200 pixel canvas (see Ex4.1-target.jpg).

The genotype used will be the x/y position of the center of the circle, it's 
radius, and the RGBA opacity of the circle (ranges from 0 to 255). 

The first step is to create a series of functions that can generate images, 
based these input circles. See the function file for these definitions.


"""
import naturalize as nat
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('..')
# import TrussAnalysis as ta
from functions import Environment, ftest, fitness, renderImg




"""
First define the environment and gene pool. The environment has been
set up to read in the base image, and define our canvas. Because the analysis
will be saved later, some dames are also defined
"""

dx = 200
dy = 200
Ncircle = 100
rmax = 10
ImageName = 'Ex4.1-target.jpg'
OutputGeneration = 'Gen_5000.P'
OutputData = 'Gen_5000_data.P'
outputGif = 'generations_M2_2.gif'
env = Environment(dx,dy,ImageName)

"""
Next a basic gene pool is defined for the problem. Four genes are used:
    [xposition, yposition, radius, opacity]
Each gene is a vector with a value for each circle
"""

llims =  [np.zeros(Ncircle), np.zeros(Ncircle), np.zeros(Ncircle), np.zeros(Ncircle) ]
ulims =  [np.ones(Ncircle)*dx, np.ones(Ncircle)*dy, np.ones(Ncircle)*rmax, np.ones(Ncircle)*255]
genePool = nat.BasicGenePool(llims, ulims)


helper = nat.AlgorithmHelper(ftest, genePool, fitness, environment = env)

"""
Next the number of individuals, couples, and survivers in the analysis is 
chosen. A small gene pool, with many couples and one surviver is used to ensure
that progress is made on the best solution. A moderate mutation rate is used, 
because the solution space is so big. A good rule of thumb is 1/N.
There are no hard rules for selecting these parameters, and other values
would be appripriate. Consider playing around the parameters to see how they 
affect the analysis.
"""

Ngen = 5000
Npop = 10
Ncouples = 3
Nsurvive = 1
mutateThresold = 0.001

algorithm = nat.GeneticAlgorithm(helper, Npop, Ncouples, Nsurvive, mutateThresold)
recorder  = nat.basicRecorder(25, 1)
analysis  = nat.Analysis(algorithm, recorder, False)
best = analysis.runAnalysis(Ngen)
bestImg = renderImg(*best, dx, dy)

"""
The results can be saved and loaded later
"""

data = analysis.getRecorderData()
nat.pickleData(analysis.currentGen, OutputGeneration)
nat.pickleData(data, OutputData)



# =============================================================================
# 
# =============================================================================

"""
Here the current score of the gene will be plotted over time. This is the sum 
of the 'net difference' between each image, that is the difference between the
'rgb' value for each pixel.
"""
plt.plot(data.genNumber, data.bestScores)
nat.plotGeneValue(data, 2, 1)


"""
Here a gif of the output is made to watch the progress of our model over time.
Not necessary but fun to see!
"""

images = []
for genotype in data.bestGenotypes:
    img = renderImg(*genotype, dx,dy)
    images.append(img)
    
images[0].save(outputGif,
               save_all = True, append_images = images[1:], 
               optimize = False, duration = 2)


