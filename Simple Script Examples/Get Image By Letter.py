#Demonstration of Getting Image by Specifying its Letter Designation
#specify the image letter
image_letter = "A"

#Find the corresponding image, and get the image data as numpy array
image = DM.FindImageByLabel(image_letter)
image_data = image.GetNumArray()
	
# Do something with image... (i.e. invert values)
image_data = (-1) * image_data

# Display result in new image
new_image = DM.CreateImage(image_data)
new_image.ShowImage()