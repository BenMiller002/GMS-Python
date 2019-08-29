#Script to Copy Image Calibrations and Tags from one image to another
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
	
#Get Front 2 Images
image_source = DM.GetFrontImage()
image_dest = image_source.FindNextImage()

#Call the function to copy everything
Calibration_and_Tag_Copy(image_source, image_dest)

print("Calibrations and Tags Copied")