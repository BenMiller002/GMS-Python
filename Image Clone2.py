def image_clone(input):
	DMImageClone = DM.CreateImage(input.GetNumArray())
	return DMImageClone
	
DMImageO = DM.GetFrontImage()

ResultImages={}
for i in range(1,3):
	ResultImages["Image{0}".format(i)] = image_clone(DMImageO)

ResultImages["Image3"].ShowImage()
