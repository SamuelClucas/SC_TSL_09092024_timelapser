#!/bin/bash

libcamera-still -n true %focus --autofocus-mode=continuous --encoding png --datetime true -o $1/at.png 2>&1 /dev/null