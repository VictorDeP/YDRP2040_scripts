'''
Miniature W2812 adressable RGB LED stoplight on YD-RP2040 microprocessor

Author: Victor De Pillecyn

Date of last change: 22/03/2023

License: Creative Commons BY (CC-BY)
//////////////////////////////////////////////////////////////////////////////////
'''



# Import necessary packages
from machine import Pin
import neopixel
import time

# Initialise 1 neopixel on pin 23
np = neopixel.NeoPixel(machine.Pin(23), 1)


while True: # Repeat indefinitely
    np[0] = (255, 0, 0) # Indicate that first neopixel (=0 in python) should be fully red
    np.write() # Don't forget this line to make the LED change color
    time.sleep(1) # Microprocessors waits 1 second
    np[0] = (255, 30, 0) # Color orange
    np.write()
    time.sleep(1)
    np[0] = (0, 255, 0) # Color green
    np.write()
    time.sleep(1)