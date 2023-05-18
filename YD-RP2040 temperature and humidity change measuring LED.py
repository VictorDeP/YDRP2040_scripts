'''
Relative humidity change indicator using DHT20 humidity and temperature sensor
on YD-RP2040 microprocessor

Author: Victor De Pillecyn

Date of last change: 22/03/2023

License: Creative Commons BY (CC-BY)
///////////////////////////////////////////////////////////////////:
'''
# Import necessary packages and modules
import neopixel
from time import sleep
from machine import Pin, I2C

# You will need to add the dht20.py file to the Rasberry pico from
# https://github.com/flrrth/pico-dht20
from dht20 import DHT20

# Set up The Serial Data (SDA) and Serial Clock (SCL) pins for I2C0 communication protocol
i2c0_sda = Pin(0)
i2c0_scl = Pin(1)
i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl)

# Initiate sensor
dht20 = DHT20(0x38, i2c0)

# Denote adressable RGB LED
np = neopixel.NeoPixel(machine.Pin(23), 1)

# Initialise parameters
measurement_number = 5 # Number of measurements/seconds to calculate the mean
measurement_array = [] # Array to keep the measurements stored
precision = 0 # Number of decimals wanted (careful, DHT20 only precise by 0.1)
change_needed = 1 # Change in relative humidity (%) needed to initialise light change

# Initial measurements
for i in range(measurement_number):
    measurement_array.append(int(dht20.measurements['rh'])) # Command to make a humidity measurement
    np[0] = ((i%2)*255, 0, (i%2)*255) # Blink between off and purple while setting up
    np.write() # Don't forget this line to make the LED change color
    sleep(1) # Sleep one second

# Check initial measurements by printing them
print(f'Initial measurements {measurement_array}')

while True:
    sleep(1)
    # Calculate mean of measurements and round off
    mean_hum = round(sum(measurement_array)/len(measurement_array), precision)
    print(f'mean humidity: {mean_hum}')
    current_hum = int(dht20.measurements['rh']) # Measure current relative humidity
    print(f'current humidity: {current_hum}')
    if current_hum > mean_hum + change_needed: # If current bigger than mean + change_needed
        np[0] = (255, 0, 0) # LED turns red
        np.write()
    elif current_hum < mean_hum - change_needed: # If current smaller than mean - change_needed
        np[0] = (0, 0, 255) # LED turns blue
        np.write()
    else:
        np[0] = (0, 255, 0) # LED turns green
        np.write()
    measurement_array.pop(0) # Remove first measurement from array
    measurement_array.append(current_hum) # Add current measurement to array