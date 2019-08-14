#Script for fitting or filtering drift measurement data
# measured from stacks in GMS. 
#The script overwrites the original data, so be sure 
# to make a copy of the data first (Edit:Duplicate Image)
#Script written by Ben Miller 
#Last updated 2019-08

import numpy as np
import scipy
from scipy.optimize import curve_fit
import scipy.signal as ss
import scipy.ndimage.filters as sf
import sys
sys.argv.extend(['-a', ' '])
import matplotlib.pyplot as plt

#User Input Section XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#Accepted FunTypes: 'Poly1' 'Poly3' 'Poly5' 'FilterSG'
#				    'FilterMed' 'FilterSmooth'
#Poly1 is a 1st degree polynomial
#FilterSG is a Savitzky-Golay Filter
#FilterMed is a median filter
#FilterSmooth is a Gaussian Smoothing (lowpass) filter
plot_external = 1
FunType = 'FilterSmooth'

#Set breakpoints (as a list in brackets) 
# this will filter sections independently
#set breakpoint to just before any sudden (real) jump
bp = []

#Set Filtering Parameters
#filterwindow=1 means window extends 1 pixel on either side: len(window)=3
filterwindow = 20
#savitzky_golay_order=2 means 2nd-order polynomial
savitzky_golay_order = 2
#gauss_sigma=1 means standard deviation for gaussian filter=1
gauss_sigma = 2

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

#Use front-most image, and get the data as numpy array
Im0 = DM.GetFrontImage()
name0 = Im0.GetName()
data_cal = Im0.GetIntensityScale()  
img0_array = Im0.GetNumArray()*data_cal
del Im0
#Create new array
img_array = np.copy(img0_array)
num_curves, sizex = img_array.shape
xdata = np.linspace(1, 2, sizex)

#If FunType entered by user is a filter, perform filtering
if FunType.find('Filter')>=0:
	#Define Filter Function Depending on Function Type Specified by User
	if FunType=='FilterSG':
		img_array[:,:]=ss.savgol_filter(img_array,
										filterwindow*2+1,savitzky_golay_order)
	elif FunType=='FilterMed':
		img_array[:,:]=ss.medfilt(img_array, kernel_size=(1,filterwindow*2+1))
	elif FunType=='FilterSmooth':
		img_array[:,:]=sf.gaussian_filter1d(img_array,
								gauss_sigma,axis=1, mode='nearest', truncate=3)
	else: 
		print('\n FunType: ' + FunType + ' is undefined. \n')	
#Otherwise, perform fitting
else:
	#For each breakpoint, fit the data leading up to that breakpoint
	#Add start and end as breakpoints
	bp.append(sizex)
	bp.insert(0,0)
	
	for i, point in enumerate(bp):
		#Skip First breakpoint, which is 0
		if i==0:
			continue 
		bp0=bp[i-1]
		bp1=bp[i]
		#Define Function Depending on Function Type Specified by User
		if FunType=='Poly1':
			def Fun(xvar,avar,bvar):
				return(avar*xvar+bvar)
		elif FunType=='Poly3':
			def Fun(x_var,a_var,b_var,c_var):
				return (a_var*x_var**2+b_var*x_var+c_var)
		elif FunType=='Poly5':
			def Fun(xvar,avar,bvar,cvar,dvar,evar):
				return (avar*xvar**4+bvar*xvar**3+cvar*xvar**2+dvar*xvar+evar)
		else:
			print('\n FunType: ' + FunType + ' is undefined. \n')
		# Fit Data using Function 
		j=0
		while j < num_curves:
			popt, pcov = curve_fit(Fun,xdata[bp0:bp1],img_array[j,bp0:bp1])
			img_array[j,bp0:bp1]=Fun(xdata[bp0:bp1],*popt)
			j+=1	


def plot2centered(ax,data,title,label):
	
	#plot center-lines and data
	ax.axvline(0,color='0.75')
	ax.axhline(0,color='0.75')
	ax.plot(data[0,:],data[1,:], label=label)
	#adjust axes
	limit = 1.1*max(np.linalg.norm(data,axis=0))
	ax.axis('scaled')
	ax.axis([-limit, limit, -limit, limit])
	#add labels
	plt.xlabel('Drift (nm)',fontsize=14)
	plt.ylabel('Drift (nm)',fontsize=14)
	plt.title(title,fontsize=12)
	#display finished plot
	
#Create new image and display it as a lineplot
imageDoc = DM.NewImageDocument("")
img1 = DM.CreateImage(img_array)
newname = (name0+" Fit Using: "+FunType)
img1.SetName(newname)
imgdsp = imageDoc.AddImageDisplay(img1, 3)
lpdsp=DM.GetLinePlotImageDisplay(imgdsp)
lpdsp.SetSliceDrawingStyle(0, 1)
imageDoc.Show()
del img1

if(plot_external):
	fig, ax = plt.subplots()
	plot2centered(ax,img_array,newname,"Fit Data")
	plot2centered(ax,img0_array,newname,"Original Data")
	ax.legend()
	plt.show()
