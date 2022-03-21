from machine import Pin, I2C, ADC
import time

#defined global variables
_up = 44068.67 #represent analog reading
_low = 17736.8

#boundarys for plant condition (percent of soil moisture)
limit_u = 65 #upper boundary (100% --> pure water)
limit_l = 45 #lower boundary (0% --> air)

#set analog pin
analog_value = ADC(28)

# function calculate relative moisture in percent
def rel_moisture(val):
    #sanity check
    if val > _up:
        print(f'Warning: measured value ({val}) greater than upper boarder ({_up})')
        val=_up
    if val < _low:
        print(f'Warning: measured value ({val}) smaller than lower boarder ({_low})')
        val=_low
    #calculate percent value
    perc = int((val-_low)*100/(_up-_low)) #between 0 and 100
    perc = 100-perc #invert the result for better readability
    print(f"Soil Moisture: {perc}% ")
    return perc

#take multiple measurements, for better accuracy
vals=[0] * 60 #create empty ist with 60 positions
for index, element in enumerate(vals): #iterate over list
    vals[index]=analog_value.read_u16() #fill list with readings
#derive the average analog measurement
val_raw = sum(vals) / len(vals)

#pass raw measurement value in relative mositure funciton to get percent value
val = rel_moisture(val_raw)
print(val)

if val < limit_u:
    #do something
    print('I need water!')
elif val > limit_l:
    #do something
    print('I am drowning!')
else:
    print('I feel fine')
