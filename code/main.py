#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Talking plant project useing the RaspberryPi Pico module.
    Copyright (C) 2022  br-mat

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
    Contact: matthiasbraun@gmx.at

Credits:
    dfplayer part based on https://github.com/lavron/micropython-dfplayermini
"""
from dfplayermini import Player
from ds3231_impl import ds3231
from machine import Pin, I2C, ADC
import time
import binascii
import sys
import random

I2C_PORT = 0
I2C_SDA = 16
I2C_SCL = 17

dry_baseline = 600
analog_value=ADC(28)

ALARM_PIN = 14

led = Pin(25, Pin.OUT)
reset = Pin(20, Pin.OUT)

#define a function to handle random tracks of specific folders, list from the dictionary need to be passed accessed by key
def pick_random_track(content_list):
    number=random.randint(1, content_list[1]) #select random number from dictionary
    music = Player(pin_TX=machine.Pin(0), pin_RX=machine.Pin(1)) #init player module
    time.sleep_ms(10)
    music.volume(40)
    #music.play(12,2)
    music.play(number, content_list[0]) #play track 1
    time.sleep(25)
    music.stop()



if __name__ == '__main__':
    led.value(0) # activate onboard LED
    rtc = ds3231(I2C_PORT,I2C_SCL,I2C_SDA) #init serial communication with RTC module
    time.sleep_ms(20) #give init process some time
    #rtc.set_time('13:26:25,Tuesday,2022-02-17') #set rtc time uncomment if needed
    #time.sleep_ms(1)
    
    #match_min=[0, 15, 30, 32, 45] #wake every list entry, keep 2 min distance!
    match_min=range(0, 59, 3) #wake every 3 min
    
    print(rtc.read_time())
    y, month, day, h, min1, sec1, wday=rtc.read_time()
    if min1 in match_min: #check for correct time
    #if True:
        print('check plant condition')
        sounds={'music': [1, 2], 'voicline_thirsty_aut': [2, 16], 'voiceline_random_aut': [3, 22]} # dictionary containing lists [folder, num tracks]
        
        #take measurement
        vals=[0]*50
        for index, element in enumerate(vals):
            vals[index]=analog_value.read_u16()
        a_read = sum(vals)/len(vals)
        
        #if _low <= a_read <= _up: #check for reasonable values
        if True:
            #if a_read > dry_baseline: #check if plant is dry
            if False:
                print('AAH! Saufen!')
                #using dictionarys as workaround for problems with folder system on the module
                pick_random_track(sounds['voicline_thirsty_aut'])
            else:
                print('plant fine!')
                #do something at random events?
                pick_random_track(sounds['voiceline_random_aut'])
                    
        else:
            print('Warning: measurement went wrong')
            #do something when measurement not working?
    
    #set next alarm
    next_index=0
    for index, element in enumerate(match_min):
        if element > min1:
            next_index=index
            break
    rtc.set_alarm1(f"{h:02}:{match_min[next_index]:02}:{sec1:02},{wday},{y:04}-{month:02}-{day:02}")
    time.sleep_ms(10)
    
    #reset FF and shutdown pico's supply
    print('shutdown')
    led.value(0)
    time.sleep_ms(10)
    reset.value(1)
