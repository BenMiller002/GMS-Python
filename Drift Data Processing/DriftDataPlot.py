import numpy as np
import sys
sys.argv.extend(['-a', ' '])
import matplotlib.pyplot as plt

def plot2centered(data,title):
	fig, ax = plt.subplots()
	ax.axvline(0,color='0.75')
	ax.axhline(0,color='0.75')
	ax.plot(data[1,:],data[0,:])
	ax.axis('scaled')
	limit = 1.1*max(np.linalg.norm(data,axis=0))
	ax.axis([-limit, limit, -limit, limit])
	plt.xlabel('Drift (nm)',fontsize=14)
	plt.ylabel('Drift (nm)',fontsize=14)
	plt.title(title,fontsize=12)
	plt.show()
	
image_0 = DM.GetFrontImage()
im_name = image_0.GetName()
data_cal = image_0.GetIntensityScale()  
array = image_0.GetNumArray()*data_cal
del image_0
plot2centered(array,im_name)
