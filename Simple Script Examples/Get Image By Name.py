#specify the image name
image_name = "untitled"

#Find the named image, and get the image data as numpy array
image = DM.FindImageByName(image_name)
image_data = image.GetNumArray()
	
# Do something with image... (i.e. invert values)
image_data = (-1) * image_data

# Display result in new image
new_image = DM.CreateImage(image_data)
new_image.ShowImage()