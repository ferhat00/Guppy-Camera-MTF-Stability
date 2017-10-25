# -*- coding: utf-8 -*-
"""
Spyder Editor

The purpose of this script is to analyse Guppy camera images that has been
used for checking the stability of the MTF test setup. 

Input to this derived from:
    - 'guppy usage Ferhat 20-9-2017.ipynb' which captures the images from the 
    Guppy in a defined sequence, where file extension ending has the time
    - 'guppy_FC.py' version is imported by the above Python .ipnyb notebook
    where the filenaming conventions can be defined for the image capture
    sequence

This script imports Guppy images in .png format, finds horizontal and
vertical slices at predefined pixel corrdinates, plots and fits logistic
function where the centre, (c-coefficient of the function, see below) is
printed out.

First open Image J and analyse one image to determine pixel range and 
coordinates to define below for analysis. Note pixel X/Y swapped round
between what you see in Image J and what Python uses.

Ferhat Culfaz 21/9/2017

"""

# Import all functions used here
import matplotlib.pyplot as plt
import numpy as np
import time
import scipy
import scipy.misc
from scipy import misc
from scipy.optimize import curve_fit
import glob
from PIL import Image
import os
import re

#%%

# Define the functions used here
def f_logistic(data, a, b, c, d):
    return a / (1 + np.exp(-b * (data - c))) + d

def detect_line(row, x):
    # Fitting a logistic to its edge response to determine the subpixel edge position
    p0 = [np.amax(row) - np.amin(row), 1, (np.amax(x) + np.amin(x)) / 2, np.amin(row)]
    popt, pcov = curve_fit(f_logistic, x, row, p0 = p0, maxfev = 10000)
    return popt

#%%
# Import the image data in png format
png = []
path = 'C:/Users/fculfaz/Python Data/20170919' # Define directory here

files = [f for f in os.listdir(path) if os.path.splitext(f)[-1] == '.png']
print(files)

# Set the range of the horizontal and vertical slices of the edges of the slit
# in pixel coordinates
x1 = 340
x2 = 370
y1 = 620
y2 = 650

#%%

edge1 = [] #Edges at X slice
edge2 = [] #Edges at Y slice
for file in files:
    im = np.array(Image.open(os.path.join(path, file)))
    
    """ Display the raw slit image"""
    
    plt.figure(1)
    plt.imshow(im); plt.show()
    plt.title('Slit Image: ' + file)
    
    print(im.shape)
    
    """ Do Horizontal Slices and set Y pixel position in first argument for the
    slice, eg 650.
    Second argument is the X pixel range set above, x1 & x2.
    """
    
    plt.figure(2)
    plt.plot(np.arange(x1, x2), im[650,x1:x2,2], label = 'Data') # Horizontal slice
    plt.title('Horizontal Cross Section')
    
    
    
    popt = detect_line(im[650,x1:x2,2], np.arange(x1, x2))
    
    x = np.linspace(x1, x2)
    y = f_logistic(x, *popt)
    
    
    plt.plot(x, y, label = 'Fit')
    plt.xlabel('x-pixels')
    plt.ylabel('ADU')
    plt.legend()
    
    # Calculate the pixel statistics for the X slices
    edge1.append(popt[2])
    mean_x = np.mean(edge1)
    sd_x = np.std(edge1)
    maxi_x = np.max(edge1)
    mini_x = np.min(edge1)
    maxi_minus_mini_x = maxi_x - mini_x
    
    """Now do Vertical Slices and set X pixel position in the second argument
    eg 370. Second argument is Y pixel range set above, y1 & y2.
    """
    
    plt.figure(3)
    plt.plot(np.arange(y1, y2), im[y1:y2,370,2], label = 'Data') # Vertical slice
    plt.title('Vertical Cross Section')
    
    popt = detect_line(im[y1:y2,370,2], np.arange(y1, y2))
    
    x = np.linspace(y1, y2)
    y = f_logistic(x, *popt)
    
    
    plt.plot(x, y, label = 'Fit')
    plt.xlabel('y-pixels')
    plt.ylabel('ADU')
    plt.legend()
    
    # Calculate the pixel statistics for the Y slices
    edge2.append(popt[2])
    mean = np.mean(edge2)
    sd = np.std(edge2)
    maxi_y = np.max(edge2)
    mini_y = np.min(edge2)
    maxi_minus_mini_y = maxi_y - mini_y

#%%
   
# Print the pixel statistics from the calculations above 
print("Centre of edges horizontally are at", edge1)
print ("The Max X is", maxi_x,"pixels")
print ("The Min X is", mini_x,"pixels")
print ("Max-Min X", maxi_minus_mini_x,"pixels")

print("Centre of edges vertically are at", edge2)
print ("The Max Y is", maxi_y,"pixels")
print ("The Min Y is", mini_y,"pixels")
print ("Max-Min Y", maxi_minus_mini_y,"pixels")

#%%

#Parse the files list to get the time part of the filename
res_list = [re.findall("-(\d+).png", fname)[0] for fname in files]
  
# Cloud plot 
plt.figure(4) 
plt.scatter(edge1,edge2)
plt.xlabel('X-pixels')
plt.ylabel('Y-pixels')
plt.title('Cloud Plot')

# Time Series plot X
plt.figure(5)
plt.plot(res_list,edge1)
plt.xlabel('Time')
plt.ylabel('X-Pixels')
plt.title('X-time series plot')

# Time Series plot Y
plt.figure(6)
plt.plot(res_list,edge2)
plt.xlabel('Time')
plt.ylabel('Y-pixels')
plt.title('Y-time series plot')
