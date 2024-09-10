#!/usr/bin/env python

"""

start_timelapse

A utility for running a timelapse based on specified input parameters.


See the help:

    timelapse --help

Usage Examples:

    Basic use:
        
"""
from ..timelapsEr.camera_controller import CameraController
from ..timelapsEr.neopixel_controller import NeopixelController as light
from ..timelapsEr.get_date import get_today, get_now

import argparse
import sys, os, time

parser = argparse.ArgumentParser(
    prog='TimelapsEr',
    description='Operator for the imaging system',
)  
parser.add_argument("-u", "--units", help="When specifying timelapse parameters, declare the units of time here for clarity. E.g. s for seconds, m for minutes, h for hours, d for days", type=str)
parser.add_argument("-d", "--duration", help="Specify the the total time period you want the system to image for. E.g. the CLI input \"-u  h -d 4\" will create a 4-hour timelapse. ", type=int)
parser.add_argument("-s", "--samples", help="Specify at how many timepoints you wish to take an image. E.g. \"-i 80\" creates a timelapse with 80 images at evenly spaced timepoints throughout the timelapse", type=int)
parser.add_argument("-p", "--path", help="Specify a file path to which the timelapse images will be saved. Default = ./\"images\"")
parser.add_argument("-n", "--name", help="Unique identifier for this timelapse", type=str)

parser.set_defaults(d = 0)
parser.set_defaults(i = 0)
parser.set_defaults(u = 's')
parser.set_defaults(p = 'Images')
parser.set_defaults(n = '')

args = parser.parse_args()

# scaling up timelapse duration to desired time unit (seconds to minutes to hours to days = x * 60 * 60 * 24)
if args.units == 'm':
    args.duration *= 60
elif args.units == 'h':
    args.duration *= 3600 
elif args.units == 'd':
    args.duration *= 86400

if args.samples != 0 and args.duration != 0: # prevents division by 0 and 0 not divisible errors
    interval = args.duration / args.samples

saveLocation = os.path.join(args.path, args.name, get_today(), get_now())

if not os.path.exists(saveLocation):
    # If current path does not exist in specified save file path, create it
    os.makedirs(saveLocation)

def timelapse(saveLocation):        
    # instantiate timelapsEr objects
    camera = CameraController(saveLocation) # configures camera module
    light = light()

    # imaging loop
    for timepoint in range(args.samples):
        light.on()

        print(f"Taking image {timepoint+1} at {get_now()}")
        camera.capture_image(timepoint+1)

        light.off()
                
        time.sleep(interval)
    # cleanup
    print("Timelapse is complete. Now exiting.")
    camera.picam2.stop()
    sys.exit(0)
    
if __name__ == '__main__':           
    timelapse(saveLocation)




