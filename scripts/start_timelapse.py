#!/usr/bin/env python
import argparse, board, neopixel
import sys, os, subprocess, time, datetime

parser = argparse.ArgumentParser(
    prog='start_timelapse.py',
    description='Operator for the imaging system',
)  
parser.add_argument("-u", "--units", help="When specifying timelapse parameters, declare the units of time here for clarity. E.g. s for seconds, m for minutes, h for hours, d for days", type=str)
parser.add_argument("-d", "--duration", help="Specify the the total time period you want the system to image for. E.g. the CLI input \"-u  h -d 4\" will create a 4-hour timelapse. ", type=int)
parser.add_argument("-s", "--samples", help="Specify at how many timepoints you wish to take an image. E.g. \"-i 80\" creates a timelapse with 80 images at evenly spaced timepoints throughout the timelapse", type=int)
parser.add_argument("-p", "--path", help="Specify a file path to which the timelapse images will be saved. Default = ./\"images\"")

parser.set_defaults(d = 0)
parser.set_defaults(i = 0)
parser.set_defaults(u = 's')
parser.set_defaults(p = 'Images')

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

saveLocation = os.path.join(args.path, str(datetime.datetime.today().strftime('%d-%m-%Y')))
if not os.path.exists(saveLocation):
    # If current path does not exist in specified save file path, create it
    os.makedirs(saveLocation)

light = neopixel.NeoPixel(board.D18, 8) 

# imaging loop
for timepoint in range(args.samples):
    light.fill((255,255,255))

    print(f"Taking image {timepoint+1} at {str(datetime.datetime.today().strftime('%Hhr%Mmin%Ssec'))}")
    
    subprocess.call(['bash', './scripts/libcamera_timelapse.sh', saveLocation, str(timepoint)])

    light.fill((0,0,0))
                
    time.sleep(interval)
# cleanup
print("Timelapse is complete. Now exiting.")

sys.exit(0)
    





