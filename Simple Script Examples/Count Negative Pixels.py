#Create Mask and Masked Version of Front Image
import numpy as np

#Get front image and image data as numpy array
img = DM.GetFrontImage()
img_data = img.GetNumArray()

#Count number of negative and total pixels 
num_negative = np.sum(np.where(img_data < 0, 1, 0))
num_total=np.product(img_data.shape)

#Print result to output window
print("Number of Negative Pixels: %s out of %s total" %(num_negative, num_total))