#!/bin/bash

libcamera-still -n true %focus --autofocus-mode=continuous --encoding png -o $1/$2  