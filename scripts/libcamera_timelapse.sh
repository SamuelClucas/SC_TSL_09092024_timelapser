#!/bin/bash

libcamera-still --autofocus-mode=continuous -e -o $1/capture_%04d.png  