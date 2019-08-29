#Demonstration of Getting Data from the Front-Most Image in GMS

#Find the front image, and get the image data as numpy array
image = DM.GetFrontImage()
image_data = image.GetNumArray()
	
# Do something with image... (i.e. invert values)
image_data = (-1) * image_data

# Display result in new image
new_image = DM.CreateImage(image_data)
new_image.ShowImage()

# The same process as above, but all in a single line 
# This gets us back to the original data
DM.CreateImage(DM.GetFrontImage().GetNumArray()*(-1)).ShowImage()