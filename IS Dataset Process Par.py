import time
import os
import sys
import numpy as np
import multiprocessing as mp
from tkinter import filedialog as tkfd
import tkinter as tk
import scipy
import scipy.ndimage.filters as sfilt
from multiprocessing.dummy import Pool as ThreadPool 
#User-Set Parameters
SIGMA = 2 #Standard Deviation of Gaussian Blur (Set to 0 for no blurring)
BINNING = 2 #Integer number of Pixels to Bin image by (Set to 1 for no binning)

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
def process_file(file):
	newfilename = file[:3] + 'DMScript Edited Datasets/' + file[3:]
	newdirname = os.path.dirname(newfilename)
	image = DM.OpenImage(file)
	imagedata = image.GetNumArray().astype('float32')
	processedimagedata = processimage(imagedata, SIGMA,BINNING)
	if not os.path.exists(newdirname):
		#print("Dir Does Not Exist")
		os.makedirs(newdirname,exist_ok=True)
	newimage=DM.CreateImage(processedimagedata)
	newimage.SaveAsGatan(newfilename)
	DM.DeleteImage(newimage)
	DM.DeleteImage(image)
	index=listOfFiles.index(file)
	if(index%20 == 0):
		print("Processed %s of %s files" % (index, num_files))
	return newfilename

start1=time.perf_counter()
threads=mp.cpu_count()
pool = ThreadPool(threads)
pool.imap(process_file, listOfFiles)    
pool.close() 
pool.join()
end1=time.perf_counter()

print("done")

start2=time.perf_counter()
for i in range(num_files):
	process_file(listOfFiles[i])
end2=time.perf_counter()
print("\nStandard Processed "+str(num_files)+" Images: Processing Time= "+str(end2-start2))
print("\nParallel Processed "+str(num_files)+" Images: Processing Time= "+str(end1-start1))
print(str(threads)+" Threads Used")