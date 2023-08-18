'''
Measure UV signal on YD-RP2040 microprocessor

Author: Victor De Pillecyn

Date of last change: 11/05/2023

License: Creative Commons BY (CC-BY)
//////////////////////////////////////////////////////////////////////////////////
'''
# Import necessary packages
import machine
import utime
import neopixel
import math
    
# Initialise 1 neopixel on pin 23
np = neopixel.NeoPixel(machine.Pin(23), 1)

# Initialise UV sensor on pin 26
sensor = machine.ADC(26)


# Physico-chemical parameters
OPL = 1 # Optical path length (cm)
MAC = 386 # Molar absorption coefficient caffeine in coffee (cm^-1M^-1)
MM_CAF = 194.19 # Molar mass caffeine in g/mol

# Volumes of coffees in L (source: https://lattelovebrew.com/coffee-cup-size-chart/)
VOLUME_ESPRESSO = 0.059
VOLUME_CAPPUCINO = 0.177
VOLUME_REGULAR = 0.25
VOLUME_LARGE = 0.35

# Define needed variables

V0 = 184 # We choose baseline voltage ourselves

NR_BLANKS = 100
BLANKS_PER_SEC = 100
BLANKS = []

MEASUREMENTS_PER_SEC = 100

    
# User setup
np[0] = (255, 30, 0)
np.write()

check = input("BLANK measurement, make sure water cuvette is installed and UV LED is on\n")

# Blank measurement
while NR_BLANKS > 0:
    np[0] = ((NR_BLANKS%5)*255, 0, 0) # Blink between off and purple while setting up
    np.write() # Don't forget this line to make the LED change color
    measurement = sensor.read_u16()
    BLANKS.append(measurement)
    NR_BLANKS -= 1
    utime.sleep(1/BLANKS_PER_SEC)
        
# Print blanks and average blank
#print(f"Blank measurements: {BLANKS}")
AVG_BLANK = round(sum(BLANKS)/len(BLANKS), 0)
print(AVG_BLANK)

while True:
    # User setup
    #check = input("Please change the cuvette to one with coffee?\n")
    MEASUREMENTS = []
    NR_MEASUREMENTS = 100
    np[0] = (255, 30, 0)
    np.write()
    print("Don't forget to shut off the UV light before opening!")
    check = input("CAFFEINE MEASUREMENT: Have you properly closed the lid and activated the UV LED?\n")
    print("Performing caffeine measurement...")

    # Cafeine measurement
    while NR_MEASUREMENTS > 0:
        np[0] = ((NR_BLANKS%5)*255, 0, 0)
        np.write()
        measurement = sensor.read_u16()
        MEASUREMENTS.append(measurement)
        NR_MEASUREMENTS -= 1
        utime.sleep(1/MEASUREMENTS_PER_SEC)
        
    # Print measurements and average measurement
    np[0] = (0, 255, 0)
    np.write()
    #print(f"Caffeine measurements: {MEASUREMENTS}")
    AVG_MEASUREMENT = round(sum(MEASUREMENTS)/len(MEASUREMENTS), 0)
    print(AVG_MEASUREMENT)
    
    if AVG_MEASUREMENT-V0 > 0:
        # Calculate absorption
        absorbance = math.log10((AVG_BLANK-V0)/(AVG_MEASUREMENT-V0))
        print(f'Absorbance: {absorbance}')

        #Calculate cafeine concentration
        
        caf_concentration = absorbance/(OPL*MAC)
        caf_massconcentration = caf_concentration*MM_CAF
        caf_ESPRESSO = abs(round(caf_massconcentration*VOLUME_ESPRESSO*1000, 0))
        caf_CAPPUCINO = abs(round(caf_massconcentration*VOLUME_CAPPUCINO*1000, 0))
        caf_REGULAR = abs(round(caf_massconcentration*VOLUME_REGULAR*1000, 0))
        caf_LARGE = abs(round(caf_massconcentration*VOLUME_LARGE*1000, 0))
        print(f'Your coffee contains {caf_concentration} mol/L')
        print(f'Depending on your coffee size, this is:\n ESPRESSO: {caf_ESPRESSO} mg\n CAPPUCINO: {caf_CAPPUCINO} mg\n REGULAR: {caf_REGULAR} mg\n LARGE: {caf_LARGE} mg')
    else:
        print(f'signal too faint :(, try again!')