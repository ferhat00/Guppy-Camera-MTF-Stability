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