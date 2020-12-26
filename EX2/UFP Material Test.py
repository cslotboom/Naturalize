# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 01:56:17 2019

@author: Christian
"""

import sys
sys.path.append('C:\\Users\\Christian\\Anaconda3\\Lib\\site-packages\\openseespy')
import opensees as op
import numpy as np
import matplotlib.pyplot as plt
import os



ExperimentStyle = {'linewidth':2, 'linestyle':'-','color':'C1'}
AnalysisStyle = {'linewidth':1, 'linestyle':'--','color':'C0'}



op.wipe()

op.model('Basic' , '-ndm',  2,  '-ndf' , 3 )


## Analysis Parameters material(s) 
## ------------------
LoadProtocol = np.array([0.00042, 0.0006, 0.0009, 0.0012, 0.0018, 0.0024, 
                         0.0036, 0.0048, 0.0073, 0.010, 0.014, 0.019, 0.028, 
                         0.04, 0.054, 0.07])
LoadProtocol = np.array([0.0017, 0.005, 0.0075, 0.012, 0.018, 0.027, 
                         0.04, 0.054, 0.068, 0.072,0.])
# Step size
dx = 0.0001


## Define material(s) 
## ------------------
Fu = 21.1*10**3
k = 2.6*10**6
b = 0.015
cR1 = .95
cR1 = .88


# test = np.array([2.47107521e+04, 6.42367587e+05, 3.57528276e-03, 1.62134442e-02, 3.90654912e-01, 1.12891881e-01])
# test = np.array([1.70715970e+04, 3.28382229e+06, 1.42308632e-02, 2.36485243e+01, 9.32352467e-01, 1.26129695e-01])
test = np.array([2.08269683e+04, 2.80002957e+06, 2.14968335e-02, 1.82111200e+01, 8.85488269e-01, 1.72870029e-01])
test = np.array([2.08269683e+04, 2.67026812e+06, 1.45697706e-02, 2.01855262e+01, 8.96729219e-01, 1.26758429e-01])
test = np.array([2.10199265e+04, 2.74529515e+06, 1.53625639e-02, 6.43325095e+00, 6.33625486e-01, 4.64405012e-02])



# op.uniaxialMaterial( 'Steel02', 1,  Fu,  k, b, 19., cR1, .15, 0.,  1.,  0.,  1.)
op.uniaxialMaterial( 'Steel02', 1, *test)


ERelease = 1.
op.uniaxialMaterial( 'Elastic' ,  2,  ERelease,  0.0 )

## Define geometric transformation(s) 
## ---------------------------------- 
#geomTransf('Linear',1) 
op.geomTransf('PDelta',1)
op.beamIntegration('Lobatto',1,1,3)

# Define geometry 
# ---------------
op.node(1,  0., 0.,  '-ndf', 3)
op.node(2,  0., 0.,  '-ndf', 3)
op.fix(1,1,1,1)

# Define element(s) 
# ----------------- 
op.element("zeroLength" , 1  , 1, 2, '-mat', 1,2,2,'-dir', 1,2,3, '-orient', 1., 0., 0., 0., 1., 0.)


# Define Recorder(s) 
# ----------------- 
op.recorder( 'Node' , '-file' , 'RFrc.out' , '-time' ,  '-nodeRange', 1,1, '-dof', 1,  2,  3 , 'reaction')
op.recorder( 'Node' , '-file' , 'Disp.out' , '-time' ,  '-nodeRange', 2,2, '-dof', 1,  2,  3 , 'disp')


# Define Analysis Parameters
# ----------------- 
op.timeSeries('Linear',1,'-factor' ,1.0)  
op.pattern  ('Plain',1, 1,  '-fact', 1.) 
op.load(2, 1.,  0.0, 0.0)

 
op.initialize() 
op.constraints("Plain")
op.numberer("Plain")
# System of Equations 
op.system("UmfPack", '-lvalueFact', 10)
# Convergence Test 
op.test('NormDispIncr',  1.*10**-8, 25, 0 , 2)
# Solution Algorithm 
op.algorithm('Newton')
# Integrator 
op.integrator('DisplacementControl', 2, 1, dx)
# Analysis Type 
op.analysis('Static')

ControlNode = 2
ControlNodeDof = 1

op.record()


# Define Analysis 
for x in LoadProtocol:
    for ii in range(0,1):
        print(ii)
        op.integrator('DisplacementControl', ControlNode, ControlNodeDof, dx)
        while (op.nodeDisp(2,1) < x):
            op.analyze(1)
            
        op.integrator('DisplacementControl', ControlNode, ControlNodeDof, -dx)
        while (op.nodeDisp(2,1) > -x):
            op.analyze(1)
        
        
op.wipe()


# =============================================================================
# Process Results
# =============================================================================

AnalysisName ='UFP Damper'
# Input Varibles
Label1="Analysis"

DisplacementFileName = 'Disp.out'
ReactionFileName = "RFrc.out"
Lable2="Experimental"
#ExperimentFileName="Backbone.csv"

OutputPlotName="Hysterisis" + AnalysisName + ".png"

PositionX=1
PositionY=1

# Create the plots 
# =============================================================================

# Create the directory names and inport the necessary files
BaseDirectory=os.getcwd()

# Create Directory name for each path
DisplacementDirectory = "%s\%s" %(BaseDirectory, DisplacementFileName)
ReactionDirectory = "%s\%s" %(BaseDirectory, ReactionFileName)

# Read Anaysis Data
DisplacementData = np.loadtxt(DisplacementDirectory,delimiter=' ')
ReactionData = np.loadtxt(ReactionDirectory,delimiter=' ')

# Load Desired Data
XData = DisplacementData[:,PositionX]
YData = -ReactionData[:,PositionY]/1000

#    # Read and Store Experimental Data
#    ExperimentDirectory="%s\%s" %(BaseDirectory, ExperimentFileName)
#    ExperimentData=np.loadtxt(ExperimentDirectory,delimiter=',',)
  
Backbonex = np.array([0, 0.004699, 0.006604, 0.0127, 0.0254, 0.07239, 0.06731, 0.062992, 0.05588, 0.0508, 0.04445, 0.0381, 0.0254, 0, -0.07239, -0.067818, -0.063754, -0.06096, -0.056388, -0.04953, -0.03302, 0, 0.0254])*1.
Backboney = np.array([0, 13.35, 16.02, 19.58, 22.25, 23.585, 8.9, 0, -7.565, -11.125, -14.24, -16.02, -18.245, -20.2475, -22.695, -8.9, 0, 4.45, 8.9, 13.35, 18.0225, 20.915, 22.25])*1000.
 

Backbonex = np.array([0.00021014, 0.002939036, 0.004758299, -0.003428387, 0.005213115, 0.006577563, 0.00794201, 0.005516326, 0.003545457, 0.000513351, -0.001457518, -0.003731597, -0.00267036, -0.001002702, 0.001726193, 0.009761274, 0.012490169, 0.003393852, -0.003731597, -0.007976545, -0.005096045, -0.000547886, 0.003393852, 0.005819536, 0.009306458, 0.013854617, 0.018705986, 0.01537067, 0.011277327, 0.006425957, 0.002181009, -0.001912334, -0.006308887, -0.01009902, -0.011766678, -0.008582967, -0.003731597, -0.001609123, 0.002332615, 0.007790405, 0.012186959, 0.018402776, 0.022950934, 0.027347488, 0.018857592, 0.014915854, 0.010974116, 0.005516326, 0.00021014, -0.005854071, -0.011311862, -0.017376074, -0.018437311, -0.014343968, -0.011311862, -0.007673335, -0.003731597, 0.001422983, 0.008093616, 0.010064485, 0.015977091, 0.020980066, 0.027347488, 0.040840359, 0.039475911, 0.035837384, 0.031744041, 0.025528224, 0.015067459, 0.007487195, -0.00267036, -0.010857046, -0.023591891, -0.027078812, -0.023440285, -0.020408179, -0.016011626, -0.011615072, -0.004489624, 0.001726193, 0.008700037, 0.015825486, 0.024921803, 0.032805279, 0.05433323, 0.049481861, 0.044175676, 0.037353437, 0.026589462, 0.013703012, -0.003125176, -0.017527679, -0.040723289, -0.040571684, -0.038297604, -0.032839814, -0.029504497, -0.025411154, -0.019650153, -0.013434336, -0.005854071, 0.006122747, 0.019009197, 0.067977707, 0.063126337, 0.058274968, 0.055091257, 0.050846308, 0.042962833, 0.038111464, 0.025376619, 0.012490169, 5.85351E-05, -0.01297952, -0.026927207, -0.043452184, -0.054367765, -0.051790475, -0.049819606, -0.048000343, -0.045574658, -0.042845763, -0.038449209, -0.032536603, -0.025411154, -0.020408179, 0.002029404, 0.013703012, 0.031289226, 0.045388518, 0.057971757, 0.066310048, 0.071767839, 0.068584128, 0.062519916, 0.057516941, 0.045994939, 0.032956884, 0.01279338, -0.001002702, -0.02071139, -0.03617513, -0.047545527, -0.068315452, -0.063464083, -0.059522345, -0.056945055, -0.053154923, -0.046029474, -0.038297604, -0.025259549, -0.013131125, 0.014612643, 0.04114357, 0.055546073, 0.07237426, 0.06721968, 0.062216705, 0.056455704, 0.04629815, 0.029924778, 0.01567388, -0.054064555, -0.071650769, -0.067860636, -0.063615688, -0.058915924, -0.053609739, -0.044816632, -0.033749445, -0.011463467, -0.00236715, 0.007032379, 0.018402776])
Backboney = np.array([0.16364747, 7.867135922, 12.63596211, -10.40113669, 13.00279489, 15.57062437, 16.30428994, 8.600801489, 3.098309738, -2.550915127, -6.219242961, -10.98806915, -5.192111168, -0.71675121, 5.079206768, 18.13845386, 19.01885254, -2.69764824, -12.38203372, -16.34382778, -7.833307208, 3.098309738, 9.994766066, 14.32339291, 17.33142173, 19.7525181, 20.48618367, 11.02189786, 1.410878934, -6.586075745, -10.91470259, -14.14283108, -15.90362844, -18.03125859, -18.32472481, -7.613207538, 2.731476954, 6.253071675, 11.90229654, 16.59775617, 19.23895221, 21.14648268, 21.51331547, 21.80678169, 0.38374714, -5.705677064, -9.887570795, -13.55589863, -15.90362844, -17.95789203, -19.27849005, -20.23225529, -19.8654225, -8.053406878, -1.303683663, 5.225939882, 10.21486574, 13.80982701, 17.33142173, 18.35855353, 20.266084, 21.51331547, 21.95351481, 22.32034759, 17.99172074, 8.160602149, -0.27655187, -8.346873105, -15.16996288, -17.15085991, -18.91165727, -20.30562184, -20.52572151, -20.8925543, -9.740837682, -1.890616117, 4.785740541, 10.14149918, 14.91032536, 17.18468862, 19.16558565, 20.70628334, 21.80678169, 22.10024792, 22.76054693, 8.747534602, -1.230317107, -9.374004899, -14.87649665, -18.10462514, -20.30562184, -21.18602052, -21.91968609, -21.25938708, -14.2895642, -2.330815457, 4.418907758, 8.820901159, 13.58972734, 16.15755683, 18.35855353, 20.41281712, 21.51331547, 23.27411283, 8.894267716, 0.16364747, -4.238345931, -8.933805559, -13.55589863, -15.4634291, -17.81115892, -19.20512349, -19.93878906, -20.74582118, -21.47948675, -21.69958642, -21.91968609, -13.18906585, -8.787072445, -4.531812157, -0.0564522, 4.492274315, 9.114367386, 13.22289456, 16.45102305, 17.84498763, 20.63291679, 21.58668202, 22.32034759, 22.54044726, 23.05401316, 23.4942125, 23.34747938, 12.26912932, -0.27655187, -6.879541971, -13.55589863, -17.29759302, -19.79205595, -20.59908807, -21.33275364, -21.91968609, -22.13978576, -22.5799851, -8.566972775, 0.016914357, 4.712373985, 8.894267716, 13.44299423, 16.59775617, 19.01885254, 19.82588466, 21.88014825, 22.61381382, 23.42084594, 23.42084594, 8.967634272, -0.49665154, -7.173008198, -13.55589863, -17.88452547, -19.57195628, -22.94681789, -22.87345133, -8.933805559, -0.0564522, 6.619904459, 11.09526442, 15.42389126, 18.13845386, 20.55955023, 20.70628334, 21.36658235, 21.95351481])*1.





font = {'fontname':'Times New Roman', 'size':'12', 'color':'black', 'weight':'normal',
              'verticalalignment':'bottom'} # Bottom vertical alignment for more space



# Plot Data
fig, ax = plt.subplots()
line2, = ax.plot(Backbonex,Backboney, label=Lable2, **ExperimentStyle)
line1, = ax.plot(XData,YData, label=Label1, **AnalysisStyle)
ax.grid(True)
#ax.set_xlim(xmin,xmax)

# plt.ylabel('Damper Force (KN)', fontname="Times New Roman")
# plt.xlabel('Horizontal Displacement (m)', fontname="Times New Roman")
# #plt.title('Damper Hystersis' )
# ax.legend(loc='lower right',fontname="Times New Roman")

plt.ylabel('Damper Force (KN)')
plt.xlabel('Horizontal Displacement (m)')
plt.title('Damper Hystersis' )

ax.legend(loc='lower right')
plt.savefig(OutputPlotName, dpi=600, )
plt.show()


# =============================================================================
# 
# =============================================================================
inches = 0.0254
kip = 4.45*10**3


import hysteresis.hys as hys

EDataName = "BackboneData.csv"
ExperimentData = np.loadtxt(EDataName,delimiter=',')

Backbonex = ExperimentData[:,0]*inches
Backboney = ExperimentData[:,1]*kip


xyExp = np.column_stack([Backbonex, Backboney])
hys3 = hys.Hysteresis(xyExp)
hys3.plot()

hys3.NCycles

xyAnal = np.column_stack([XData, YData*1000])
hys4 = hys.Hysteresis(xyAnal)

hys4.plot()

out = hys.CompareHys(hys3, hys4)
out = hys.CompareHys(hys4, hys3)
print(hys3.NCycles)