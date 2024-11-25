#!/usr/bin/env python
"""
Timelapse Camera Control System

This script controls a camera system for creating timelapses using a NeoPixel LED ring for illumination.
It allows specification of timelapse duration, number of samples, and save location, with configurable
time units (seconds, minutes, hours, days).

Dependencies:
    - board: For hardware GPIO access
    - neopixel: For LED control
    - argparse: For CLI argument parsing
    - subprocess: For executing camera capture commands
"""

import argparse
import board
import neopixel
import sys
import os
import subprocess
import time
import datetime

def setup_argument_parser() -> argparse.ArgumentParser:
    """
    Configure and return the argument parser for CLI options.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser with timelapse options
    """
    parser = argparse.ArgumentParser(
        prog='start_timelapse.py',
        description='Operator for the imaging system',
    )
    
    parser.add_argument(
        "-u", "--units",
        help="Time units for timelapse parameters (s: seconds, m: minutes, h: hours, d: days)",
        type=str
    )
    parser.add_argument(
        "-d", "--duration",
        help="Total time period for imaging (e.g., -u h -d 4 creates a 4-hour timelapse)",
        type=int
    )
    parser.add_argument(
        "-s", "--samples",
        help="Number of images to capture at evenly spaced intervals",
        type=int
    )
    parser.add_argument(
        "-p", "--path",
        help="File path for saving timelapse images (default: ./Images)",
        type=str
    )

    # Set default values
    parser.set_defaults(d=0)
    parser.set_defaults(s=0) 
    parser.set_defaults(u='s')
    parser.set_defaults(p='Images')

    return parser

def convert_duration_to_seconds(duration: int, units: str) -> int:
    """
    Convert the specified duration to seconds based on the time unit.
    
    Args:
        duration (int): The time duration specified
        units (str): Time unit (s: seconds, m: minutes, h: hours, d: days)
    
    Returns:
        int: Duration converted to seconds
    """
    if units == 'm':
        return duration * 60
    elif units == 'h':
        return duration * 3600 
    elif units == 'd':
        return duration * 86400
    return duration  # Default to seconds

def ensure_directory_exists(path: str) -> None:
    """
    Create the specified directory if it doesn't exist.
    
    Args:
        path (str): Directory path to check/create
    """
    if not os.path.exists(path):
        os.makedirs(path)

def setup_neopixel() -> neopixel.NeoPixel:
    """
    Initialize and return the NeoPixel LED ring.
    
    Returns:
        neopixel.NeoPixel: Configured NeoPixel object
    """
    return neopixel.NeoPixel(board.D18, 8)

def capture_image(timepoint: int, path: str, light: neopixel.NeoPixel) -> None:
    """
    Capture a single image with LED illumination.
    
    Args:
        timepoint (int): Current image number in sequence
        path (str): Directory to save the image
        light (neopixel.NeoPixel): NeoPixel LED object for illumination
    """
    # Turn on LED illumination
    light.fill((255, 255, 255))

    print(f"Taking image {timepoint+1}. Saving in format 'MMDDhhmmss.png'.")
    
    # Capture image using external script
    subprocess.call(['bash', './scripts/libcamera_still_capture.sh', path])

    # Turn off LED illumination
    light.fill((0, 0, 0))

def main() -> None:
    """
    Main function to run the timelapse capture system.
    """
    # Parse command line arguments
    parser = setup_argument_parser()
    args = parser.parse_args()

    # Convert duration to seconds based on specified units
    duration_seconds = convert_duration_to_seconds(args.duration, args.units)

    # Initialize interval
    interval = 0
    
    # Calculate interval between images if both parameters are non-zero
    if args.samples != 0 and duration_seconds != 0:
        interval = duration_seconds / args.samples

    # Ensure save directory exists
    ensure_directory_exists(args.path)

    # Initialize LED ring
    light = setup_neopixel()

    # Capture timelapse images
    for timepoint in range(args.samples):
        capture_image(timepoint, args.path, light)
        time.sleep(interval)

    print("Timelapse is complete. Now exiting.")
    sys.exit(0)

if __name__ == "__main__":
    main()