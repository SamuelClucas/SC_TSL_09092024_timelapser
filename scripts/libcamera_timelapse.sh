#!/bin/bash

libcamera-still --autofocus-mode=continuous -e --datetime -o $1/capture_%04d.png  