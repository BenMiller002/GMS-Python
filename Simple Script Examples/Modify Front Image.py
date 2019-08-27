#Find the front image, and modify the data within that image
#Get Front image and then the data as a numpy array
image = DM.GetFrontImage()
image_data = image.GetNumArray()
	
# Do something with image... (i.e. invert values)
image_data[:,:] = (-1) * image_data

#Update the Image Display
image.UpdateImage()
