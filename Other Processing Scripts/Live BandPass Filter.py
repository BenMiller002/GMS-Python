#GUI-Based Band-Pass Filter
#Use Sliders to Set the Inner and Outer Limits for the BandPass Filter
#Use 3rd Slider to Set the Weighting of Original and Filtered Data in the Final Output Image
#Close the GUI Window to End the Script
import numpy as np
import sys
sys.argv.extend(['-a', ' '])
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from scipy import fftpack as SFFT
from scipy import ndimage
from scipy import signal
from scipy.ndimage.interpolation import geometric_transform

def create_circular_mask(h, w, center=None, radius=None):
	if center is None: # use the middle of the image
		center = [int(w/2), int(h/2)]
	if radius is None: # use the smallest distance between the center and image walls
		radius = min(center[0], center[1], w-center[0], h-center[1])

	Y, X = np.ogrid[:h, :w]
	dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

	mask = dist_from_center <= radius
	return mask.astype('int')

#Funtion to convert cartesian-coordinate image to polar-coordinate image
def topolar(img,  r_size, theta_size, order=1):
	sx, sy = img.shape
	max_radius = int(sx/2)
	#define transform
	def transform(coords):
		theta = 2.0*np.pi*coords[1] / (theta_size - 1.)
		radius = max_radius * coords[0] / r_size
		i = int(sx/2) - radius*np.sin(theta)
		j = radius*np.cos(theta) + int(sx/2)
		return i,j
	#perform transform
	polar = geometric_transform(img, transform, output_shape=(r_size,theta_size), order=order,mode='constant',cval=1.0,prefilter=False)	
	return polar
#Function to calculate radial profile of FFT from image
def FFT_radial_profile(image_o, profile_res):	
	#compute FFT
	fft_im = np.absolute(SFFT.fftshift(SFFT.fft2(image_o)))
	#Median-Filter FFT to remove single-pixel outliers
	#fft_im_median=scipy.ndimage.median_filter(fft_im, size=3)
	fft_im_median=fft_im
	#determine profile size
	sx, sy = fft_im.shape
	profile_size = int(sx/sizefraction)
	#convert FFT image to polar coordinates
	polar_im = topolar(fft_im_median, profile_size, profile_res, order=1)
	#compute radial mean and maximum profiles
	labels = np.mgrid[1:profile_size+1,1:profile_res+1]
	index = np.arange(1,profile_size+1)
	radial_max = ndimage.measurements.maximum(polar_im, labels=labels[0,:,:],index=index)
	radial_mean = ndimage.measurements.mean(polar_im, labels=labels[0,:,:],index=index)
	#median-filter the radial mean profile to smooth this further
	radial_mean_median = signal.medfilt(radial_mean)
	#radial profile is radial-max minus radial-mean
	radial_profile = radial_max-radial_mean_median
	return radial_profile

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
	
orig_im = DM.GetFrontImage()
orig_name = orig_im.GetName()
orig_im_array = orig_im.GetNumArray()
live_im_array=SFFT.fftshift(SFFT.fft2(orig_im_array))
live_im_array_copy=np.copy(live_im_array)
live_fft_image = DM.CreateImage(np.absolute(live_im_array))
live_fft_image.SetName("FFT of "+orig_name)
live_fft_image.ShowImage()
live_fft_array = live_fft_image.GetNumArray()
live_fft_array_copy = np.copy(live_fft_array)
filt_image = DM.CreateImage(orig_im_array)
filt_image.SetName("FFT Filtered "+orig_name)
filt_image.ShowImage()
filt_im_array = filt_image.GetNumArray()

sizefraction = 2
angle_res = 512
rad_profile = np.log(FFT_radial_profile(orig_im_array,angle_res))

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)

l, = plt.plot(np.linspace(0,1,len(rad_profile)),rad_profile)
rad_inner_0 = 0.25
rad_outer_0 = 0.5
delta_f = 0.005
lim_out = ax.axvline(color='k')
lim_out.set_xdata(rad_outer_0)
lim_in = ax.axvline(color='k')
lim_in.set_xdata(rad_inner_0)
plt.draw()
ax.margins(x=0)

axcolor = 'silver'
outer_slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
inner_slider_ax = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
amp_slider_ax = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)

outer_slider = Slider(outer_slider_ax, 'Outer', 0, 1.0, valinit=rad_outer_0, valstep=delta_f)
inner_slider = Slider(inner_slider_ax, 'Inner', 0, 1.0, valinit=rad_inner_0, valstep=delta_f)
filt_amp_slider = Slider(amp_slider_ax, 'Fraction Filtered', 0, 1.0, valinit=.5, valstep=delta_f)
#Get image dimensions
w = live_fft_array.shape[1]
h = live_fft_array.shape[0]
min_dim = min(w,h)
CENTER=None

def update(val):
	OUTER_RADIUS_FRACTION=outer_slider.val
	INNER_RADIUS_FRACTION=inner_slider.val
	Filtered_FRACTION=filt_amp_slider.val
	rad_out = OUTER_RADIUS_FRACTION*min_dim/2
	rad_in = INNER_RADIUS_FRACTION*min_dim/2
	lim_in.set_xdata(INNER_RADIUS_FRACTION)
	lim_out.set_xdata(OUTER_RADIUS_FRACTION)
	
	#Create mask
	mask_data = create_circular_mask(h, w, center=CENTER, radius=rad_out)
	mask_data = mask_data*(1-create_circular_mask(h, w, center=CENTER, radius=rad_in))
	live_fft_array[:,:] = np.where(mask_data, live_fft_array_copy, 0)
	live_im_array[:,:]= np.where(mask_data, live_im_array_copy, 0)
	filt_im_array[:,:] = SFFT.ifft2(SFFT.fftshift(live_im_array))*Filtered_FRACTION+orig_im_array*(1-Filtered_FRACTION)
	filt_image.UpdateImage()
	fig.canvas.draw_idle()
	live_fft_image.UpdateImage()
	plt.draw()

outer_slider.on_changed(update)
inner_slider.on_changed(update)
filt_amp_slider.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    outer_slider.reset()
    inner_slider.reset()
    filt_amp_slider.reset()
button.on_clicked(reset)

plt.show()
plt.clf()
plt.close()

Calibration_and_Tag_Copy(orig_im,filt_image)