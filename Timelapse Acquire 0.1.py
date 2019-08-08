camera = DM.GetActiveCamera( )  
image1 = camera.CreateImageForAcquire(1, 1, 1)  
image1.ShowImage()
camera.StartContinuousAcquisition(0.1, 1, 1, 1)  
for i in range(5):
	DM.Sleep(2)
	camera.GetFrameInContinuousMode(image1, 5)
	image1.UpdateImage()  
	
camera.StopContinuousAcquisition()  
