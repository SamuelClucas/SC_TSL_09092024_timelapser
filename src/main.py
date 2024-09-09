from camera.camera_controller import CameraController
from lighting.neopixel_controller import NeopixelController
from motor.motor_controller import MotorController
import argparse
import sys, os, time
import datetime
from picamera2 import Picamera2, Preview
from libcamera import controls


class ImagingSystem:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='ImagingSystem',
            description='Operator for the imaging system',
        )  
        self.parser.add_argument("-t", "--timelapse", help="Initiate a timelapse. See manual for additional parameters.", action='store_true')

        self.parser.add_argument("-u", "--units", help="When specifying timelapse parameters, declare the units of time here for clarity. E.g. s for seconds, m for minutes, h for hours, d for days", type=str)
        self.parser.set_defaults(u = 's')

        self.parser.add_argument("-d", "--duration", help="Specify the the total time period you want the system to image for. E.g. the CLI input \"-u  h -d 4\" will create a 4-hour timelapse. ", type=int)
        self.parser.set_defaults(d = 0)
        

        self.parser.add_argument("-s", "--samples", help="Specify at how many timepoints you wish to take an image. E.g. \"-i 80\" creates a timelapse with 80 images at evenly spaced timepoints throughout the timelapse", type=int)
        self.parser.set_defaults(i = 0)

        self.parser.add_argument("-p", "--path", help="Specify a file path to which the timelapse images will be saved. Default = ./\"images\"")
        self.parser.set_defaults(p = 'images')

        self.parser.add_argument("-n", "--name", help="Unique identifier for your timelapse", type=str)

        self.args = self.parser.parse_args()

        # scaling up timelapse duration to desired time unit (seconds to minutes to hours to days = x * 60 * 60 * 24)
        if self.args.units == 'm':
            self.args.duration *= 60
        elif self.args.units == 'h':
            self.args.duration *= 3600 
        elif self.args.units == 'd':
            self.args.duration *= 86400

        if self.args.samples != 0 and self.args.duration != 0:
            self.interval = self.args.duration / self.args.samples
        
        self.currentDate = str(datetime.datetime.today().strftime('%d-%m-%Y'))

        self.saveLoc = os.path.join(self.args.path, self.currentDate)

        if not os.path.exists(self.args.path):
            os.makedirs(self.args.path)

        if not os.path.exists(self.args.path + "/" + self.currentDate):
            # If current date directory does not exist in specified save file path, create it
            os.makedirs(self.saveLoc)
        
        self.cameraController = CameraController(self.saveLoc) # configures camera module
        self.lightController = NeopixelController()
        self.motorController = MotorController()
        
    def timelapse(self):
        for timepoint in range(self.args.samples):
            self.lightController.on()

            print(f"Taking image {timepoint+1} at {str(datetime.datetime.today().strftime('%H:%M:%S'))}")
            self.cameraController.capture_image(timepoint+1)

            self.lightController.off()
            
            time.sleep(self.interval)
        self.cleanup()

    def cleanup(self):
        print("Timelapse is complete. Now exiting.")
        self.cameraController.picam2.stop()
        sys.exit(0)
            
system = ImagingSystem()
system.timelapse()



