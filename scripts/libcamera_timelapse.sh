#!/bin/bash

libcamera-still -n %focus --autofocus-mode=continuous --encoding png -o $1/capture_%04d.png  