from picamera2 import Picamera2, Preview
from libcamera import controls
from timelapsEr import get_date
import numpy as np
'''
See documentation here: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

'''

class CameraController:
    def __init__(self, path):
        self.saveLocation = path
        # initialise camera
        self.picam2 = Picamera2()

        self.picam2.start_preview(Preview.NULL) 
        
        self.config = self.picam2.create_still_configuration() 
        
        self.picam2.set_controls({"AfMode": controls.AfModeEnum.Auto, "AeEnable": True, "AwbEnable": True})
        
        self.picam2.options["quality"] = 95
        print(self.config["main"])
        
        self.picam2.configure(self.config)
        
        self.picam2.start()

        

    def capture_image(self, timepoint):
        # capture image logic 

        imageArray = self.picam2.capture_array("main")  
        np.shape(imageArray)    

        gy, gx = np.gradient(imageArray)
        gnorm = np.sqrt(gx**2 + gy**2)
        sharpness = np.average(gnorm)
        print(sharpness)
                               
        success = self.picam2.autofocus_cycle()
        request = self.picam2.capture_request(flush=True)
        metadata = request.get_metadata()
        lensPos = metadata.get("LensPosition")
        print(lensPos)
        
        request.save("main", f"{self.saveLocation}/image_{timepoint}_at_{get_date.get_now()}.png") # illegal filename characters n

        request.release()
