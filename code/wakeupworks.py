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
"""

from machine import Pin, I2C
import time
import binascii
import sys

#    the new version use i2c0,if it dont work,try to uncomment the line 14 and comment line 17
#    it should solder the R3 with 0R resistor if want to use alarm function,please refer to the Sch file on waveshare Pico-RTC-DS3231 wiki
#    https://www.waveshare.net/w/upload/0/08/Pico-RTC-DS3231_Sch.pdf
I2C_PORT = 0
I2C_SDA = 16
I2C_SCL = 17

ALARM_PIN = 14

led2 = Pin(15, Pin.OUT)
test=0
led = Pin(25, Pin.OUT)
reset = Pin(20, Pin.OUT)

class ds3231(object):
#            00:53:19 Tue 25 Jan 2022
#  the register value is the binary-coded decimal (BCD) format
#               sec min hour week day month year
    NowTime = b'\x00\x53\x19\x00\x25\x01\x22'
    w  = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    address = 0x68
    start_reg = 0x00
    ALARM1_REG = 0x07
    ALARM2_REG = 0x11
    control_reg = 0x0e
    status_reg = 0x0f
    
    def __init__(self,i2c_port,i2c_scl,i2c_sda):
        time.sleep_ms(1)
        self.bus = I2C(i2c_port,scl=Pin(i2c_scl),sda=Pin(i2c_sda), freq=100000)
        time.sleep_ms(1)
        
    def set_time(self,new_time):
        hour = new_time[0] + new_time[1]
        minute = new_time[3] + new_time[4]
        second = new_time[6] + new_time[7]
        week = "0" + str(self.w.index(new_time.split(",",2)[1])+1)
        year = new_time.split(",",2)[2][2] + new_time.split(",",2)[2][3]
        month = new_time.split(",",2)[2][5] + new_time.split(",",2)[2][6]
        day = new_time.split(",",2)[2][8] + new_time.split(",",2)[2][9]
        now_time = binascii.unhexlify((second + " " + minute + " " + hour + " " + week + " " + day + " " + month + " " + year).replace(' ',''))
        #print(binascii.unhexlify((second + " " + minute + " " + hour + " " + week + " " + day + " " + month + " " + year).replace(' ','')))
        #print(self.NowTime)
        self.bus.writeto_mem(int(self.address),int(self.start_reg),now_time)
    
    def read_time(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        y="20%x" %t[6]
        mon="%02x" %t[5]
        d="%02x" %t[4]
        h="%02x" %t[2]
        m="%02x" %t[1]
        s="%02x" %t[0]
        wday=self.w[t[3]-1]
        print("time: " + "20%x-%02x-%02x %02x:%02x:%02x %s" %(t[6],t[5],t[4],t[2],t[1],t[0],self.w[t[3]-1]))
        #         y        month     d       h       m      s      wday
        return ((int(y), int(mon), int(d), int(h), int(m), int(s), wday))
        
    @staticmethod
    def interupt_handler(cls):
        print("handler triggered")
        #rtc.set_alarm_time('21:23:50,Tuesday,2022-01-25')
        led.toggle()
        led2.value(1)
        #_buf=bytearray(1)
        #print(cls.bus.readfrom_mem_into(cls.address, cls.control_reg, _buf))
        # Clear alarm flag bit
        #cls.bus.writeto_mem(cls.address, cls.control_reg, b'\~x05')
        #print(cls.bus.readfrom_mem_into(cls.address, cls.control_reg, _buf))


    def set_alarm_time(self,alarm_time):
        print("alarm set")
        print(alarm_time)
        #    init the alarm pin
        #self.alarm_pin = Pin(ALARM_PIN,Pin.IN,Pin.PULL_UP)
        #    set alarm irq
        #self.alarm_pin.irq(handler = self.interupt_handler, trigger = Pin.IRQ_FALLING)
        

        #    convert to the BCD format
        hour = alarm_time[0] + alarm_time[1]
        minute = alarm_time[3] + alarm_time[4]
        second = alarm_time[6] + alarm_time[7]
        date = alarm_time.split(",",2)[2][8] + alarm_time.split(",",2)[2][9]
        now_time = binascii.unhexlify((second + " " + minute + " " + hour +  " " + date).replace(' ',''))
        print(now_time)
        #    write alarm time to alarm1 reg
        
        self.bus.writeto_mem(int(self.address),int(self.ALARM1_REG),now_time)
        
        # clear alarm1 flag
        self.bus.writeto_mem(self.address, self.control_reg, b'\~x05')

        #    enable the alarm1 reg
        self.bus.writeto_mem(int(self.address),int(self.control_reg),b'\x05')

        
if __name__ == '__main__':
    led.value(0)
    rtc = ds3231(I2C_PORT,I2C_SCL,I2C_SDA)
    time.sleep_ms(10)
    #rtc.set_time('13:27:25,Tuesday,2022-02-17')
    #time.sleep_ms(1)
    match_min=[0, 15, 30, 32, 45]
    print(rtc.read_time())
    y, month, day, h, min1, sec1, wday=rtc.read_time()
    if min1 in match_min:
        led.value(1) #activate onboard led
        time.sleep(10)
    
    next_index=0
    for index, element in enumerate(match_min):
        if element > min1:
            next_index=index
            break

    rtc.set_alarm_time(f"{h:02}:{match_min[next_index]:02}:{sec1:02},{wday},{y:04}-{month:02}-{day:02}")
    time.sleep_ms(10)
    led.value(0)
    reset.value(1)
