#Script for Visualizing the Effect of Poisson Noise in Counted Images
#Inputs are the mean # of electron counts per pixel per frame and the
# number of such frames to be summed together
#The script uses the front-most image in GMS. 
#IMPORTANT!! This image should have as little noise as possible!

#Script written by Ben Miller
#Last Modified Sep 2018

import numpy as np

import sys
sys.argv.extend(['-a', ' '])

import matplotlib.pyplot as plt

MEANeCOUNTS=5
SUMFRAMES=1

img = DM.GetFrontImage()
image_a = img.GetNumArray().astype(float)
orig_name=img.GetName()
new_name=orig_name+": Poisson Avg e- Count= {}".format(MEANeCOUNTS*SUMFRAMES)

noisy=0*image_a
for i in range(0, SUMFRAMES):
    noisy_i = np.random.poisson(image_a / np.mean(image_a) * MEANeCOUNTS)
    noisy=noisy+noisy_i

img2 = DM.CreateImage(noisy)
img2.SetName(new_name)
img2.ShowImage()

plt.figure(1)
plt.subplot(1, 2, 1)
plt.hist(image_a.flatten(),bins=512)
plt.gca().set_title('Original Image Histogram')

plt.subplot(1, 2, 2) 
poissonbins = np.minimum(int(MEANeCOUNTS*SUMFRAMES*20),512)
plt.hist(noisy.flatten(),bins=poissonbins,facecolor='g')
plt.gca().set_title('Poisson Noise Image Histogram')
plt.show()