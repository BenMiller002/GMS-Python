#Create Mask and Masked Version of Front Image
import numpy as np

#Get front image and image data as numpy array
img = DM.GetFrontImage()
img_data = img.GetNumArray()

#Create mask based on image mean
mask_data = np.where(img_data > np.mean(img_data), 1, 0)
mask_img = DM.CreateImage(mask_data)

#Name and display mask image
mask_img.SetName("Binary mask for " + img.GetName())
mask_img.ShowImage()

#Create, Name, and Display masked image
img_masked = DM.CreateImage(np.where(mask_data, img_data, 0))
img_masked.SetName(img.GetName() + " masked")
img_masked.ShowImage()

#delete images that are no longer needed (will not delete original image)
del img
