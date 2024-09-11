from picamera2 import Picamera2, Preview
from libcamera import controls
from timelapsEr import get_date
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
        
        #self.picam2.set_controls({"AeEnable": True, "AwbEnable": True, "FrameRate": 1.0, "AfMode": controls.AfModeEnum.Continuous}) # from Alison's camera_project
        self.picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 0.0}
        self.picam2.options["quality"] = 95
        print(self.config["main"])
        
        #self.config.align() # optimises stream size alignment
        self.picam2.configure(self.config)
        
        self.picam2.start()

        

    def capture_image(self, timepoint):
        # capture image logic 

        #imageArray = self.picam2.capture_array("main")  \ if in future you want to pass the images directly to opencv as arrays, see here*
        #np.shape(imageArray)                             

        request = self.picam2.capture_request(flush=True)
        metadata = request.get_metadata()
        print(request.get_metadata())
        
        request.save("main", f"{self.saveLocation}/image_{timepoint}_at_{get_date.get_now()}.png") # illegal filename characters n

        request.release()
