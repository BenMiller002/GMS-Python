#Find the front image, and get the image data as numpy array
image1 = DM.GetFrontImage()
image1_data = image1.GetNumArray()

#Find the next image, and get its image data as numpy array
image2 = image1.FindNextImage()
image2_data = image2.GetNumArray()

# Do something with image... (i.e. invert values)
image1_data = (-1) * image1_data
image2_data = (-1) * image2_data

# Display results in 2 new images
new_image1 = DM.CreateImage(image1_data)
new_image2 = DM.CreateImage(image2_data)
new_image1.ShowImage()
new_image2.ShowImage()

# The same process as above, but all in 3 lines 
# This gets us back to the original data
image3 = DM.GetFrontImage()
DM.CreateImage(image3.GetNumArray()*(-1)).ShowImage()
DM.CreateImage(image3.FindNextImage().GetNumArray()*(-1)).ShowImage()