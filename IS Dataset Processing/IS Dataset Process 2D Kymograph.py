'''
Python Script for processing data in a Gatan IS video dataset produced with a Gatan IS camera.
The script computes a profile along the same line-ROI for every frame in the video dataset. 

To use the script, open the desired dataset with the IS player, and place an ROI on the displayed frame. 
(It does not matter which video frame is displayed when placing this ROI.)
With this window front-most, run the script, and select the base folder of the same dataset using the 
provided file dialog. 

Script written by Ben Miller 
Last Updated 2019-11
'''
 
import numpy as np
import scipy
import os
import sys
import tkinter as tk
import tkinter.filedialog as tkfd
from numpy import linalg as LA
import scipy.ndimage

#User-Set Parameters
#(None for now)

# Let User Select the IS Dataset Directory
sys.argv.extend(['-a', ' '])
root = tk.Tk()
root.withdraw() #use to hide tkinter window
currdir = os.getcwd()
dirname = tkfd.askdirectory(parent=root, initialdir=currdir, title='Please select the IS Dataset Root Directory')
if len(dirname) > 0:
    print("Original IS DataSet Directory: %s" % dirname)
    os.chdir(dirname)

# Get the list of all files in directory tree at given path
listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk(dirname):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]

# Function to Process the Image Data in Each Image and Produce a Vector
def processimage(numpy_data, lr):
	#Produce a profile line from an image and 4 coordinates
	x_y_length=[lr[2]-lr[0],lr[3]-lr[1]]
	num=np.trunc(LA.norm(x_y_length)).astype('int')
	#Produce line coordinates
	x, y = np.linspace(lr[0], lr[2], num), np.linspace(lr[1], lr[3], num)
	coords=np.vstack((y,x))
	# Extract the values along the line, using cubic interpolation
	processed_output=scipy.ndimage.map_coordinates(numpy_data, coords)
	return(processed_output)
	

#Get line ROI from Front-Most Image
roi_im = DM.GetFrontImage()
roi_disp = roi_im.GetImageDisplay(0)
num_rois = roi_disp.CountROIs()
#If an ROI is selected, get this one, otherwise get 1st ROI
for r in range(num_rois):
    if roi_disp.IsROISelected(roi_disp.GetROI(r)):
        roi = roi_disp.GetROI(r)
        break
    else:
        roi = roi_disp.GetROI(0)
#If line ROI is found, get coordinates, otherwise prompt user and stop script
try:
	left, top, right, bottom = roi.GetLine()
	line_ROI=roi.GetLine()
except:
	DM.OkDialog( 'Error: No ROI Found. \n\nBefore Running this Script, Select an Image with an ROI' )
	print('\nError: No ROI Found. Script Stopped. \nBefore Running this Script, Select an Image with an ROI')
	sys.exit()

#Get Name of Original Dataset from one of the images
middle_image = DM.OpenImage(listOfFiles[len(listOfFiles)//2])
name_orig=middle_image.GetName()
#Just keep first part of image name (before "_Hour_00_Minute_00...")
name_orig=name_orig[:name_orig.find("_Hour")]

#Main loop over all image files in dataset
i=0
for file in listOfFiles:
	if i%5==0: print("Processing Image %s" %i)
	#Open image and get data
	image = DM.OpenImage(file)
	imagedata = image.GetNumArray()
	#Process image
	processedimagedata = processimage(imagedata, line_ROI)
	if i==0:
		#If this is the first image, create array for data to be placed in
		(sy,) = processedimagedata.shape
		result_data = np.zeros((sy,len(listOfFiles)))
		print("Result Data Shape"+ str(result_data.shape))
		result_data[:,i]  = processedimagedata
	else:
		result_data[:,i]  = processedimagedata
	#Delete image to free up memory
	del image
	i=i+1
#Create and display image from results array
result_image = DM.CreateImage(result_data)
result_image.SetName("Line Profile of "+name_orig)
result_image.ShowImage()

#Delete python images to free up memory (displayed images will still be available in GMS)
del roi_im
del result_image
del middle_image
