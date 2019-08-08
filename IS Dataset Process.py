import tkinter as tk
import tkinter.filedialog as tkfd
import os
import sys
import scipy
import scipy.ndimage.filters as sfilt

#User-Set Parameters
SIGMA = 2 #Standard Deviation of Gaussian Blur

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

# Function to Process the Image Data in Each Image 
def processimage(numpy_data, sigma):
	def bindata(img, binning):
		shape=(img.shape[0]//binning,binning,img.shape[1]//binning,binning)
		return img.reshape(shape).mean(-1).mean(1)
	processed_data = bindata(sfilt.gaussian_filter(numpy_data, sigma),2)
	return processed_data

#Get data type of original data
middle_image = DM.OpenImage(listOfFiles[len(listOfFiles)//2])
dtype=npDType(middle_image.GetDataType())
print("Data Type= %s" % dtype)

#Main loop over all image files
i=0
for file in listOfFiles:
	i=i+1
	newfilename = file[:3] + 'DMScript Edited Datasets/' + file[3:]
	newdirname = os.path.dirname(newfilename)
	image = DM.OpenImage(file)
	imagedata = image.GetNumArray()
	processedimagedata = processimage(imagedata, SIGMA)
	if not os.path.exists(newdirname):
		print("Dir Does Not Exist")
		os.makedirs(newdirname)
	newimage=DM.CreateImage(processedimagedata.astype(dtype))
	newimage.SaveAsGatan(newfilename)
	DM.DeleteImage(newimage)
	DM.DeleteImage(image)
	print("Saved Image %s" % i)
print("Processed Data Directory: %s" % newdir )