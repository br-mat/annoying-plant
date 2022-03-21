from machine import Pin, I2C, ADC

#set analog pin
analog_value = ADC(28)

#defined global variables
_up = 44068.67 #represent analog reading in air
_low = 17736.8 #analog reading while in water

#take multiple measurements, for better accuracy
vals=[0] * 60 #create empty ist with 60 positions
for index, element in enumerate(vals): #iterate over list
    vals[index]=analog_value.read_u16() #fill list with readings
#derive the average analog measurement
val_raw = sum(vals) / len(vals)

print(val_raw)