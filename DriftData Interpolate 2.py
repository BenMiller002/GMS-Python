#Script for interpolating drift measurement data
# measured from stacks in GMS. 
#This is useful for summing frames in a stack, then 
# measuring the drift of the summed data, then interpolating
# this measurement using this script and finally using 
# the interpolated data to drift correct the original dataset

#Script written by Ben Miller 
#Last updated 2019-08

import numpy as np
import scipy
from scipy.interpolate import interp1d

#User Defined Parameters
binning=1
multiple=2

#Get data from front-most image
image_0=DM.GetFrontImage()
im_name=image_0.GetName()
array=image_0.GetNumArray()

#Get Number of points
numsig, numpoints = array.shape
numpointsnew=numpoints*multiple

#Get Data as vectors
array=image_0.GetNumArray()*binning
y1 = array[0,:]
y2 = array[1,:]
x = np.linspace(0, numpoints-1, num=numpoints)

#Interpolate Data as Vectors and Place in new array
f1 = interp1d(x, y1, kind='linear',fill_value='extrapolate')
f2 = interp1d(x, y2	, kind='linear',fill_value='extrapolate')
xnew = np.linspace(0, numpoints-1, num=numpointsnew)
newarray=np.zeros([2,numpointsnew])
newarray[0,:]=f1(xnew)
newarray[1,:]=f2(xnew)

#Create new image and display as lineplot
img1 = DM.CreateImage(newarray)
imageDoc = DM.NewImageDocument("")
img1.SetName("Interpolated "+im_name)
imgdsp = imageDoc.AddImageDisplay(img1, 3)
lpdsp=DM.GetLinePlotImageDisplay(imgdsp)
lpdsp.SetSliceDrawingStyle(0, 1)
imageDoc.Show()

#Copy Tags
oldtags = image_0.GetTagGroup()
newtags = img1.GetTagGroup()
newtags.SetTagAsTagGroup('Original Tags',oldtags.Clone()) 

print('Data Interpolated to %s Frames' % numpointsnew)