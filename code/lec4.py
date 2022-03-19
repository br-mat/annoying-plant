from machine import Pin, I2C, ADC
import time

#defined global variables
_up = 44068.67
_low = 17736.8
limit = 30000.0

#set analog pin
analog_value = ADC(28)

# function calculate relative moisture in percent
def moisture(val):
    perc = int(100-(val-_low)*100/(_up-_low)) #between 0 and 100
    print(f"Soil Moisture: {perc}% ")
    return perc

#take multiple measurements
vals=[0] * 60 #create list with 60 positions
for index, element in enumerate(vals): #iterate over list
    vals[index]=analog_value.read_u16() #fill list with readings
val = sum(vals) / len(vals) #derive the average

#decide if measurement is ok
print (moisture (val))
#print (val)
if _low <= val <= _up:
    if val > limit:
        #do something
        print('I need water!')
    else:
        print('I feel fine ... maybee to ')
else:
    print(f'Warning: Measurement went wrong {val}')
