The programme at Checkpoint_1 can take a few arguments from the CLI as inputs to image at set intervals within a specified duration of time. These images are saved to the specified path.

The camera settings need to be adjusted, as during the night the images became extremely overexposed by the neopixel lights (see tests directory). This will be especially noticeable when fit inside an incubator, given it will be totally dark prior to taking images.

Further to this, depth of field needs to be corrected. The images are blurry. This is likely due to the focus being modified somehow by previous use of the camera module, as out of the box the camera should be set to infinite depth of field by default. See documentation here: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

Currently the parser doesn't meaningfully use some of the arguments it creates namespaces for. This is to be implemented in checkpoint 2.

Finally, I must validate that the images are indeed being taken exactly at the specified frequency for the duration of the timelapse. This could simply be added to the standard output message printed on each loop of the timelapse method.

It should also be noted the structure of the programme isn't fixed in stone. At this stage, it looks like this (if viewing on github, change to 'Code' view):

imaging_system/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── camera/
│   │   ├── __init__.py
│   │   └── camera_controller.py
│   ├── lighting/
│   │   ├── __init__.py
│   │   └── neopixel_controller.py
│   ├── motor/
│       ├── __init__.py
│       └── motor_controller.py
│
├── tests/
│   ├── __init__.py
│   ├── test_camera.py
│   ├── test_lighting.py
│   └── test_motor.py
│
├── requirements.txt
├── setup.py
