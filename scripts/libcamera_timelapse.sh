#!/bin/bash

libcamera-still -n true %focus --autofocus-mode=continuous --encoding png -o $1/DD_hh_mm.png 2>&1 /dev/null