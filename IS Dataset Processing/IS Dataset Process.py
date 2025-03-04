#Script written by Ben Miller
#Last Modified Aug 2019

import tkinter as tk
import tkinter.filedialog as tkfd
import os
import sys
import scipy
import scipy.ndimage.filters as sfilt
import time
import numpy as np
#User-Set Parameters
SIGMA = 2 #Standard Deviation of Gaussian Blur
BINNING = 2
# Function to Specify Data Type
def npDType(DM_type_num):
	np_type="float32" #Default if type not in list below
	if DM_type_num==6: np_type="uint8"
	if DM_type_num==10: np_type="uint16"
	if DM_type_num==11: np_type="uint32"
	if DM_type_num==2: np_type="float32"
	if DM_type_num==12: np_type="float64"
	if DM_type_num==3: np_type="complex64"
	if DM_type_num==13: np_type="complex128"
	return np_type
	
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

#Get data type of original data
num_files=len(listOfFiles)
middle_image = DM.OpenImage(listOfFiles[num_files//2])
dtype=npDType(middle_image.GetDataType())
print("Data Type= %s" % dtype)

# Function to Process the Image Data in Each Image 
def processimage(numpy_data, sigma, binning):
	#Binning Function
	#If width or height are not integer multiple of binning value, 
	#the first few rows/columns are deleted to make them integer multiples
	def bindata(img, binning):
		def simplebin(img,binning):
			shape=(img.shape[0]//binning,binning,img.shape[1]//binning,binning)
			return img.reshape(shape).mean(-1).mean(1)*binning**2
			
		if(binning==1):
			return img
		else:
			remy = img.shape[0]%binning
			remx = img.shape[1]%binning
			if(remy+remx)==0:
				return simplebin(img,binning)
			elif(remy==0):
				img=np.delete(img,list(range(remx)),1)
				return simplebin(img,binning)
			elif(remx==0):
				img=np.delete(img,list(range(remy)),0)
				return simplebin(img,binning)
			else:
				img=np.delete(img,list(range(remx)),1)
				img=np.delete(img,list(range(remy)),0)
				return simplebin(img,binning)
	try:
		if(sigma>0):
			processed_data = bindata(sfilt.gaussian_filter(numpy_data, sigma),binning)
		elif(sigma==0):
			processed_data = bindata(numpy_data,binning)
		return processed_data
	except (RuntimeError, TypeError, NameError, ValueError):
		print("processimage function Failed ")

start=time.perf_counter()
#Main loop over all image files
i=0
for file in listOfFiles:
	i=i+1
	newfilename = file[:3] + 'DMScript Edited Datasets/' + file[3:]
	newdirname = os.path.dirname(newfilename)
	image = DM.OpenImage(file)
	imagedata = image.GetNumArray().astype('float32')
	processedimagedata = processimage(imagedata, SIGMA,BINNING)
	if not os.path.exists(newdirname):
		print("Dir Does Not Exist")
		os.makedirs(newdirname)
	newimage=DM.CreateImage(processedimagedata)
	newimage.SaveAsGatan(newfilename)
	DM.DeleteImage(newimage)
	DM.DeleteImage(image)
	if(i%10==1 or num_files<20): print("Saved Image %s" % i)
print("Processed Data Directory: %s" % newdir )
end=time.perf_counter()
print("\n Processed "+str(num_files)+" Images: Processing Time= "+str(end-start))