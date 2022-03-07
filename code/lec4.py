from machine import Pin, I2C, ADC
import time

#defined global variables (replace values)
_up = 3000
_low = 1000
threshold = 1500 #example value


analog_value = ADC(28)

#take multiple measurements
vals=[0] * 60 #create list with 60 positions
for index, element in enumerate(vals): #iterate over list
    vals[index]=analog_value.read_u16() #fill list with readings
val = sum(vals) / len(vals) #derive the average

#decide if measurement is ok
if _low <= val <= _up:
    if val > limit:
        #do something
        print('do something')
    else:
        print('I feel fine')
else:
    print('Warning: Measurement went wrong')