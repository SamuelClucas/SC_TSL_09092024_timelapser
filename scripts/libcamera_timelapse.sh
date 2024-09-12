#!/bin/bash
filename="$($capture_%0d.png" "$1")"

libcamera-still -n true %focus --autofocus-mode=continuous --encoding png -o $1/$filename  