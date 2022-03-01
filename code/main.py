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
from machine import Pin, I2C
import time
import binascii
import sys
import random

#    the new version use i2c0,if it dont work,try to uncomment the line 14 and comment line 17
#    it should solder the R3 with 0R resistor if want to use alarm function,please refer to the Sch file on waveshare Pico-RTC-DS3231 wiki
#    https://www.waveshare.net/w/upload/0/08/Pico-RTC-DS3231_Sch.pdf
I2C_PORT = 0
I2C_SDA = 16
I2C_SCL = 17

dry_baseline = 600

ALARM_PIN = 14

led = Pin(25, Pin.OUT)
reset = Pin(20, Pin.OUT)

#insert class ds3231 if needed
        
if __name__ == '__main__':
    led.value(0) # activate onboard LED
    rtc = ds3231(I2C_PORT,I2C_SCL,I2C_SDA) #init serial communication with RTC module
    time.sleep(1) #give init process some time
    #rtc.set_time('13:26:25,Tuesday,2022-02-17') #set rtc time uncomment if needed
    #time.sleep_ms(1)
    
    match_min=[0, 15, 30, 32, 45] #wake every list entry, keep 2 min distance!
    #match_min=range(0, 59, 3) #wake every 3 min
    
    print(rtc.read_time())
    y, month, day, h, min1, sec1, wday=rtc.read_time()
    if min1 in match_min: #check for correct time
    #if True:
        print('check plant condition')
        if a_read > dry_baseline:
            print('AAH! Saufen!')
            #using dictionarys as workaround for problems with folder system on the module
            sounds={'music': [1, 2], 'voicline_at':[3,4,5,6,7,8,9,10]} # dictionary containing lists
            number_i=random.randint(1, len(sounds['voicline_at'])) #select random number from dictionary
            number=sounds['voicline_at'][number_i]
            music = Player(pin_TX=machine.Pin(0), pin_RX=machine.Pin(1)) #init player module
            time.sleep_ms(10)
            music.module_wake()
            time.sleep_ms(10)
            music.volume(50)
            music.play(number) #play track 1
            time.sleep(15)
            #music.pause()
            music.module_sleep()
        else:
            print('plant fine!')
    
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
