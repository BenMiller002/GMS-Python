import numpy as np
import sys
import os
import time
import ast
import tkinter as tk
import tkinter.filedialog as tkfd
sys.argv.extend(['-a', ' '])
import matplotlib.pyplot as plt

#Get Info From Image Tags
def GetK3TagDataAsString(image):
	tg = image.GetTagGroup()
	bval, areastr = tg.GetTagAsString( "Acquisition:Parameters:High Level:CCD Read Area")
	area = ast.literal_eval(areastr)
	size=(area[2]-area[0],area[3]-area[1])
	bval, processing = tg.GetTagAsString( "Acquisition:Parameters:High Level:Processing")
	bval, binning = tg.GetTagAsString( "Acquisition:Parameters:High Level:Binning")
	bval, exp_time = tg.GetTagAsUInt32( "Acquisition:Parameters:High Level:Exposure (s)")
	bval, read_mode = tg.GetTagAsUInt32( "Acquisition:Parameters:High Level:Read Mode")
	read_modes = ['Non-CDS Linear', 'Non-CDS Counting','CDS Linear','CDS Counting']
	info_str = str(read_modes[read_mode])+", "+processing+", "+str(exp_time)+"s exp, \nSize: "+str(size)+", Binning: "+binning
	return(info_str)


def PlotStatsAsBox(image,ax):
	
	#Set Defect Pixel Thresholds
	lim1=1.1
	lim2=2
	
	#Get pixel data and info from tags
	info_str = GetK3TagDataAsString(image)
	array = image.GetNumArray()
	data = array.ravel()

	#Get Some Basic Stats
	median = np.median(data)
	range=np.ptp(np.log10(data))
	
	#Plot Data
#	ax.violinplot(data, showmedians=True,showmeans=True)
	ax.boxplot(np.log10(data))
	
	#Add text labels
	lim1str=str(lim1)
	lim2str=str(lim2)
	ax.axhline(np.log10(median*lim1), color='g',linestyle='--')
	ax.text(1.5,np.log10(median*lim1)-range*.02,lim1str+' x Median', color='g',ha='right')
	ax.axhline(np.log10(median*lim2), color='b',ls='--')
	ax.text(1.5,np.log10(median*lim2)-range*.02,lim2str+' x Median', color='b',ha='right')
	ax.set_title(info_str,fontsize=10)
	num_lim1 = np.sum(data>median*lim1)
	num_lim2 = np.sum(data>median*lim2)
	left,r = ax.get_xlim()
	ax.text(left,np.log10(median*lim1*1.01),str(num_lim1)+" Pixels above        "+lim1str+" * Median")
	ax.text(left,np.log10(median*lim2*1.01),str(num_lim2)+" Pixels above        "+lim2str+" * Median")

#Have User Specify Files to Include
root = tk.Tk()
root.withdraw() #use to hide tkinter window
currdir = os.getcwd()
filez = tkfd.askopenfilenames(parent=root,title='Choose up to 4 files')

#Sort files by size
file_list = root.tk.splitlist(filez)
files_by_size = []
for file in file_list:
    size = os.path.getsize(file)
    files_by_size.append((size, file))
files_by_size.sort(key=lambda s: s[0],reverse=True)

#Create Figure and plot one axis for each file
fig, ax = plt.subplots(1,len(file_list),figsize=(16.0, 10.0))
i=0
for file in files_by_size:
	image = DM.OpenImage(file[1])
	PlotStatsAsBox(image,ax[i])
	i+=1

#Save, then Display, Figure	
folder=os.path.dirname(file_list[0])
save_name=folder+'/K3 IS Pixel Stats Box Plots.png'
plt.savefig(save_name)
print("Figure Saved as "+save_name)
plt.show(block=False)
plt.pause(5)
print("Click anywhere in figure to close and end script")
plt.waitforbuttonpress()
plt.close('all')
