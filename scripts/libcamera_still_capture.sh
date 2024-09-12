#!/bin/bash

libcamera-still -n true %focus --autofocus-mode=continuous --encoding png --datetime true -o $1 2>/dev/null