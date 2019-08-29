#Crop Center of Image to Specified Size
import numpy as np

#Specify Final Image Size
size_x_out = 512
size_y_out = 780


#Function to Copy calibrations and tags from one image to another
def Calibration_and_Tag_Copy(image_source, image_dest):
	#Count and check that number of dimensions match
	num_dim_s = image_source.GetNumDimensions()
	num_dim_d = image_dest.GetNumDimensions()
	if num_dim_d != num_dim_s:
		DM.OkDialog('Images do not have same number of dimensions!')
		return 
		
	#Copy Dimension Calibrations
	origin = [0 for _ in range(num_dim_s)]
	scale = origin
	power = origin
	unit = ["" for _ in range(num_dim_s)]
	unit2 = unit
	for i in range(num_dim_s):
		origin[i], scale[i], unit[i] =  image_source.GetDimensionCalibration(i, 0)
		image_dest.SetDimensionCalibration(i,origin[i],scale[i],unit[i],0)
		unit2[i], power[i] = image_source.GetDimensionUnitInfo(i)
		image_dest.SetDimensionUnitInfo(i,unit2[i],power[i])
	
	#Copy Intensity Calibrations
	i_scale = image_source.GetIntensityScale()
	i_unit = image_source.GetIntensityUnitString()
	i_origin = image_source.GetIntensityOrigin()
	image_dest.SetIntensityScale(i_scale)
	image_dest.SetIntensityUnitString(i_unit)
	image_dest.SetIntensityOrigin(i_origin)
	
	#Copy Tags
	tg_source = image_source.GetTagGroup()
	tg_dest = image_dest.GetTagGroup()
	tg_dest.SetTagAsTagGroup("Copied Tags",tg_source.Clone())
	

#Find the front image, and get the image data as numpy array
image = DM.GetFrontImage()
image_data = image.GetNumArray()

#Get input image sixe and center
sx,sy = image_data.shape
center_x = sx//2
center_y = sy//2

#Print info to Output Window
print("Current Image is %s x %s pixels" %(sx,sy))
print("Cropped Image is %s x %s pixels" %(size_x_out,size_y_out))

#Check sizes
if (size_x_out <= sx) & (size_y_out <= sy):
	#Get top-left corner coordinates
	x_min = center_x-size_x_out//2
	y_min = center_y-size_y_out//2
	#Get cropped image data
	im_cropped_data = np.copy(image_data[y_min:y_min+size_y_out,x_min:x_min+size_x_out])
	#Create new image from numpy array
	im_cropped = DM.CreateImage(im_cropped_data)
	#Copy calibrations and tags to the cropped image
	Calibration_and_Tag_Copy(image, im_cropped)
	#Display cropped image
	im_cropped.ShowImage()
else: print("Cropped size is larger than original image")
	

