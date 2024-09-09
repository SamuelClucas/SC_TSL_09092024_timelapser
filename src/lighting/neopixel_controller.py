import board, neopixel
import time
import sys

# Documentation: https://docs.circuitpython.org/projects/neopixel/en/latest/
# See guide here: https://thepihut.com/blogs/raspberry-pi-tutorials/using-neopixels-with-the-raspberry-pi?srsltid=AfmBOop8FCIniAOPGgAvqOdNrJBvGcflZbIhPGeNI91ULHHpDQtYILzR
class NeopixelController:
    def __init__(self):
        self.light = neopixel.NeoPixel(board.D18, 8) #(board.D18, 30) if breaks

    def on(self):
         self.light.fill((255,255,255))
        
    def off(self):
         self.light.fill((0,0,0))

    def flash(self):  
            self.light.fill((255,255,255))
            time.sleep(1.5)
            self.light.fill((0,0,0))
            time.sleep(1.5)

    