#Create New Image in GMS with Script-Generated Data
#Creates an image of a Spiral Galaxy
import numpy as np
from scipy import signal

#Specify User-Set Parameters (500, 1024, 4) are recommended for first try
#Larger values for any of these parameters will increase the time required
NUM_STARS_PER_ARM = 500
IMAGE_SIZE = 1024
KERN_SIZE = 4

#Calculate all star positions
n = NUM_STARS_PER_ARM
b = 0.6
th = np.random.randn(n)
x = np.exp(b*th)*np.cos(th)
y = np.exp(b*th)*np.sin(th)
x1 = np.exp(b*(th))*np.cos(th+np.pi)
y1 = np.exp(b*(th))*np.sin(th+np.pi)
sx = np.random.normal(0, 0.25, n)
sy = np.random.normal(0, 0.25, n)
xc = np.concatenate(((x+sy),(x1+sx)))
yc = np.concatenate(((y+sx),(y1+sy)))
dmax = 1.01*max(max(np.abs(xc)),max(np.abs(yc)))

#Create an exponential kernal used to produce intensity gradient around each star
def create_exp_kernel(size):
	x = np.arange(-size, size)
	y = np.arange(-size, size)
	xx, yy = np.meshgrid(x, y)
	r = np.sqrt(xx**2+yy**2)
	return(np.exp(-2*r))

#Initialize images before starting for-loop 
sx = IMAGE_SIZE
kern = create_exp_kernel(KERN_SIZE)
blank_image = np.zeros((sx,sx))
image_data = np.copy(blank_image)
pointimage = np.copy(blank_image)
#Loop over each star 
for star in range(len(xc)):
	#add star position as single pixel 
	px = int(np.fix(xc[star]/dmax*sx/2)+sx//2)
	py = int(np.fix(yc[star]/dmax*sx/2)+sx//2)
	pointimage[px,py] = 1
	#once every 50 stars, convolve the single-pixel image with the kernel 
	#to generate a single image frame and add this to the final image_data array
	if star % 50 == 0:
		image_data += signal.convolve2d(pointimage, kern, mode='same')
		#reset the single-pixel image so it is blank again
		pointimage = np.copy(blank_image)
		#print progress to the Output Window in GMS
		print("Processed %s points" %star)
	
DM.CreateImage(image_data).ShowImage()