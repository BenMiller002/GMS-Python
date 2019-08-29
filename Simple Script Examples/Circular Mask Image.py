#Create Circularly Masked Version of Front Image
import numpy as np

#Set Radius as fraction of the image size (from center to the nearest edge)
RADIUS_FRACTION = .5

#Set the center of the circle as (x,y). 
#If CENTER = None, the center of the image is used
CENTER = None
#CENTER = (300,800)


def create_circular_mask(h, w, center=None, radius=None):

    if center is None: # use the middle of the image
        center = [int(w/2), int(h/2)]
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask.astype('int')

#Get front image and image data as numpy array
img = DM.GetFrontImage()
img_data = img.GetNumArray()

#Get image dimensions
w = img_data.shape[1]
h = img_data.shape[0]
min_dim = min(w,h)
rad = RADIUS_FRACTION*min_dim/2

#Create mask based on image mean
mask_data = create_circular_mask(h, w, center=CENTER, radius=rad)
mask_img = DM.CreateImage(mask_data)

#Name and display mask image
mask_img.SetName("Binary mask for " + img.GetName())
mask_img.ShowImage()

#Create, Name, and Display masked image
img_masked = DM.CreateImage(np.where(mask_data, img_data, 0))
img_masked.SetName(img.GetName() + " masked")
img_masked.ShowImage()

#delete images that are no longer needed (will not delete original image)
del img