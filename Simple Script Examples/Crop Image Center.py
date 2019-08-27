import numpy as np
#Find the front image, and get the image data as numpy array
image = DM.GetFrontImage()
image_data = image.GetNumArray()

#Get Calibration Info
origin0, scale0, unit0 = image.GetDimensionCalibration(0, 0)
origin1, scale1, unit1 = image.GetDimensionCalibration(1, 0)
i_scale = image.GetIntensityScale()
i_unit = image.GetIntensityUnitString()
i_origin = image.GetIntensityOrigin()
#Get input image sixe and center
sx,sy = image_data.shape
center_x = sx//2
center_y =sy//2

#Set Final Image size
size_x_out = 512
size_y_out = 780


#Check sizes
if (size_x_out <= sx) & (size_y_out <= sy):
	x_min = center_x-size_x_out//2
	y_min = center_y-size_y_out//2
	im_cropped_data = np.copy(image_data[y_min:y_min+size_y_out,x_min:x_min+size_x_out])
	im_cropped = DM.CreateImage(im_cropped_data)
	
	im_cropped.SetDimensionCalibration(0,origin0,scale0,unit0,0)
	im_cropped.SetDimensionCalibration(1,origin1,scale1,unit1,0)
	im_cropped.SetIntensityScale(i_scale)
	im_cropped.SetIntensityUnitString(i_unit)
	im_cropped.SetIntensityOrigin(i_origin)
	im_cropped.ShowImage()
else: print("Cropped size is larger than original image")
	

