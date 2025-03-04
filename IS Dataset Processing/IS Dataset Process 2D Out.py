#Script written by Ben Miller
#Last Modified Aug 2019

import inspect
import numpy as np
import os
import sys
import time
import tkinter as tk
import tkinter.filedialog as tkfd
import scipy
from scipy import ndimage
from scipy import signal
from scipy import fftpack
from scipy.ndimage.interpolation import geometric_transform
import scipy.ndimage.filters as sfilt

test=0

if(test): print("line %s" %inspect.currentframe().f_lineno)
	

#User-Set Parameters
Profile_Resolution = 200 

# Let User Select the IS Dataset Directory
sys.argv.extend(['-a', ' '])
root = tk.Tk()
root.withdraw() #use to hide tkinter window
currdir = os.getcwd()
dirname = tkfd.askdirectory(parent=root, initialdir=currdir, title='Please select the IS Dataset Root Directory')
if len(dirname) > 0:
    print("Original IS DataSet Directory: %s" % dirname)
    newdir=dirname[:3] + 'DMScript Edited Datasets/' + dirname[3:]
    os.chdir(dirname)

# Get the list of all files in directory tree at given path
listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk(dirname):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]

# Function to Process the Image Data in Each Image 
def processimage(numpy_data, profile_res):
	if(test): print("line %s" %inspect.currentframe().f_lineno)
	#Funtion to convert cartesian-coordinate image to polar-coordinate image
	def topolar(img,  r_size, theta_size, order=1):
		if(test): print("line %s" %inspect.currentframe().f_lineno)
		sx, sy = img.shape
		max_radius = int(sx/2)
		#define transform
		def transform(coords):	
			#if(test): print("line %s" %inspect.currentframe().f_lineno)
			theta = 2.0*np.pi*coords[1] / (theta_size - 1.)
			radius = max_radius * coords[0] / r_size
			i = int(sx/2) - radius*np.sin(theta)
			j = radius*np.cos(theta) + int(sx/2)
			return i,j
		#perform transform
		polar = geometric_transform(img, transform, output_shape=(r_size,theta_size), order=order,mode='constant',cval=1.0,prefilter=False)	
		return polar

	#Function to calculate radial profile of FFT from image
	def FFT_radial_profile(image_o, profile_res):	
		if(test): print("line %s" %inspect.currentframe().f_lineno)
		sizefraction=2
		#compute FFT
		fft_im = np.absolute(scipy.fftpack.fftshift(scipy.fftpack.fft2(image_o)))
		#Median-Filter FFT to remove single-pixel outliers
		#fft_im_median=scipy.ndimage.median_filter(fft_im, size=3)
		fft_im_median=fft_im
		#determine profile size
		sx, sy = fft_im.shape
		profile_size = int(sx/sizefraction)
		#convert FFT image to polar coordinates
		polar_im = topolar(fft_im_median, profile_size, profile_res, order=1)
		#compute radial mean and maximum profiles
		labels = np.mgrid[1:profile_size+1,1:profile_res+1]
		index = np.arange(1,profile_size+1)
		radial_max = ndimage.measurements.maximum(polar_im, labels=labels[0,:,:],index=index)
		radial_mean = ndimage.measurements.mean(polar_im, labels=labels[0,:,:],index=index)
		#median-filter the radial mean profile to smooth this further
		radial_mean_median = scipy.signal.medfilt(radial_mean)
		#radial profile is radial-max minus radial-mean
		radial_profile = np.atleast_2d(radial_max-radial_mean_median)	
		return radial_profile
		
	processed_data = FFT_radial_profile(numpy_data, profile_res)
	return processed_data

#Main loop over all image files
i=0
for file in listOfFiles:
	print("Processing Image %s" %i)
	image = DM.OpenImage(file)
	imagedata = image.GetNumArray()
	processedimagedata = processimage(imagedata, Profile_Resolution)
	if i==0:
		sx, sy = processedimagedata.shape
		print(sy)
		result_data = np.zeros((sy,len(listOfFiles)))
		print(result_data.shape)
		result_data[:,i]  = processedimagedata
	else:
		result_data[:,i]  = processedimagedata
	DM.DeleteImage(image)
	i=i+1
result_image = DM.CreateImage(result_data)
result_image.ShowImage()