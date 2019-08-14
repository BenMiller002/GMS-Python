#Simple script to perform Gaussian blurring on the front image
#Script written by Ben Miller
#Last Modified Aug 2019

import scipy.ndimage.filters as sfilt

SIGMA=2

def process_image(numpy_data, sigma):
	return sfilt.gaussian_filter(numpy_data, sigma)

image_data = DM.GetFrontImage().GetNumArray()
processed_data = process_image(image_data, SIGMA)
new_image = DM.CreateImage(processed_data)
new_image.ShowImage()

print("Gaussian Blur Performed with Sigma = %s Pixels" %SIGMA)