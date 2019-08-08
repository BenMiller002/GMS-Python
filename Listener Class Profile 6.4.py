import numpy as np
import time
import sys
import scipy
from scipy import ndimage
from scipy import signal
from scipy import fftpack
from scipy.ndimage.interpolation import geometric_transform

class CListen(DM.Py_ScriptObject):
	#Initialization Function
	def __init__(self, img):
		self.name = "ImageO"
		self.angleres=512
		self.sizefraction=4
		self.i = 0
		self.j = True #this is only for IS player testing
		#get the original image and assign it to self.imgref
		self.imgref = img
		#get the shape and calibration of the original image
		(input_sizex, input_sizey) = img.GetNumArray()[0:2044,0:2044].shape
#		origin, self.scale, self.unit_stringo = self.imgref.GetDimensionCalibration(0, 0)
#		self.diff_scale=1/self.scale/input_sizex
#		self.unit_string=self.unit_stringo+"-1"
		r_img_size=int(input_sizex/self.sizefraction)
		#create empty set for result images
		self.result_images = {}
		#create 1st result image and set calibration
		self.result_images[self.name] = DM.CreateImage(np.copy(np.zeros((r_img_size,20))))
#		self.result_images[self.name].SetDimensionCalibration(1,0,self.diff_scale,self.unit_string,0)
		self.result_images[self.name].ShowImage()		
		#get numpy array from result image
		self.result_array = self.result_images[self.name].GetNumArray()
		DM.Py_ScriptObject.__init__(self)
		print("Constructor (in Python) for CListen2...")
		
	#Function to end Image Listener
	def __del__(self):
		DM.Py_ScriptObject.__del__(self)
		print("destructor (in Python) for CListen .. removed from memory")
	
	#Funtion to convert cartesian-coordinate image to polar-coordinate image
	def topolar(self, img,  r_size, theta_size, order=1):
		sx, sy = img.shape
		max_radius = int(sx/2)
		#define transform
		def transform(coords):
			theta = 2.0*np.pi*coords[1] / (theta_size - 1.)
			radius = max_radius * coords[0] / r_size
			i = int(sx/2) - radius*np.sin(theta)
			j = radius*np.cos(theta) + int(sx/2)
			return i,j
		#perform transform
		polar = geometric_transform(img, transform, output_shape=(r_size,theta_size), order=order,mode='constant',cval=1.0,prefilter=False)	
		return polar
	
	#Function to calculate radial profile of FFT from image
	def FFT_radial_profile(self, image_o, profile_res):	
		#compute FFT
		fft_im = np.absolute(scipy.fftpack.fftshift(scipy.fftpack.fft2(image_o)))
		#Median-Filter FFT to remove single-pixel outliers
		#fft_im_median=scipy.ndimage.median_filter(fft_im, size=3)
		fft_im_median=fft_im
		#determine profile size
		sx, sy = fft_im.shape
		profile_size = int(sx/self.sizefraction)
		#convert FFT image to polar coordinates
		polar_im = self.topolar(fft_im_median, profile_size, profile_res, order=1)
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
	
	#This function is run each time the image changes
	def HandleDataChangedEvent(self, flags, image):
			if self.j: #this is only for IS player testing
				#start timing
				start=time.perf_counter()
				self.j = not self.j #this is only for IS player testing
				(result_sizex, result_sizey) = self.result_array.shape
				#if the result image is nearly full, make it 2x larger
				if self.i > result_sizey-2:
					#create a new numpy array 2x larger
					self.result_array_temp = np.append(self.result_array, np.zeros_like(self.result_array), axis=1)
					#close the old results image in DM
					DM.DeleteImage(self.result_images[self.name])
					print("ImageDeleted")
					#create a new results image and calibrate it
					self.name="Image{0}".format(self.i)
					self.result_images[self.name] = DM.CreateImage(np.copy((self.result_array_temp)))
#					self.result_images[self.name].SetDimensionCalibration(1,0,self.diff_scale,self.unit_string,0)
					print("ImageCreated")
					#display new result image in DM
					self.result_images[self.name].ShowImage()	
					#get numpy array from new result image
					self.result_array = (self.result_images[self.name].GetNumArray())
				#print("Result Array Shape:")
				#print(self.result_array.shape)
				#compute radial FFT profile from the image, and place this profile into results image
				self.result_array[:,self.i]  = (self.FFT_radial_profile(self.imgref.GetNumArray()[0:2044,0:2044], self.angleres))
				self.result_images[self.name].UpdateImage()
				#print("RadialProfile Generated")
				#end timing and output time to process this frame
				end=time.perf_counter()
				print("Processed Image "+str(self.i)+"  Processing Time= "+str(end-start))
				self.i = self.i+1	
			else: 
				self.j = not self.j #this is only for IS player testing
	#Function to end script if source image window is closed
	def HandleWindowClosedEvent(self, event_flags, window):
		print("Window Closed")
		self.__del__()
		print("Script Ended")		
#Main Code Starts Here
#Get front image in GMS		
img1 = DM.GetFrontImage()
#Get the image window, so we can check if it gets closed
imageDoc = DM.ImageGetOrCreateImageDocument(img1)
imDocWin = imageDoc.GetWindow()
#initiate the image listener
listener = CListen(img1)
#check if the source window closes
listener.WindowHandleWindowClosedEvent(imDocWin, 'pythonplugin')
#check if the source image changes
listener.ImageHandleDataChangedEvent(img1, 'pythonplugin')