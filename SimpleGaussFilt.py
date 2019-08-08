import scipy
import scipy.ndimage.filters as sfilt

def processimage(numpy_data, sigma):
	print("Processing")
	processed_data = sfilt.gaussian_filter(numpy_data, sigma)
	print("Processed")
	return processed_data

imagedata = DM.GetFrontImage().GetNumArray()
processedimagedata = processimage(imagedata, 2)
newimage=DM.CreateImage(processedimagedata)
newimage.ShowImage()
print("Done")