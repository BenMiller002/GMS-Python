#Demonstration of Getting an Image by Specifying its ID

#First get the ID of the front image (to get an ID guaranteed to be valid)
front_image_ID = DM.GetFrontImage().GetID()

#Now prompt the user to enter any ID number, 
#  providing the front-image ID as a suggested value
DM.GetNumber("Get Image with ID=",front_image_ID)

#Find the image with this ID, and get the image data as numpy array
image = DM.FindImageByID(front_image_ID)
image_data = image.GetNumArray()
	
# Do something with image... (i.e. invert values)
image_data = (-1) * image_data

# Display result in new image
new_image = DM.CreateImage(image_data)
new_image.ShowImage()