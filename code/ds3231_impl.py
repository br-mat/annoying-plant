import time
import binascii
from machine import Pin, I2C

class ds3231(object):
#            00:53:19 Tue 25 Jan 2022
#  the register value is the binary-coded decimal (BCD) format
#               sec min hour week day month year
    c_time = b'\x00\x53\x19\x00\x25\x01\x22' #example
    w  = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    address = 0x68
    start_reg = 0x00
    alarm1_reg = 0x07
    alarm2_reg = 0x11
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

    def set_alarm1(self,alarm_time):
        print("alarm 1 set")
        print("at:", alarm_time)
        #  convert to the BCD format
        hour = alarm_time[0] + alarm_time[1]
        minute = alarm_time[3] + alarm_time[4]
        second = alarm_time[6] + alarm_time[7]
        date = alarm_time.split(",",2)[2][8] + alarm_time.split(",",2)[2][9]
        now_time = binascii.unhexlify((second + " " + minute + " " + hour +  " " + date).replace(' ',''))
        print(now_time)
        
        # write alarm time to alarm1 reg
        self.bus.writeto_mem(int(self.address),int(self.alarm1_reg),now_time)
        
        # clear alarm1 flag
        self.bus.writeto_mem(self.address, self.control_reg, b'\~x05')

        # enable the alarm1 reg
        self.bus.writeto_mem(int(self.address),int(self.control_reg),b'\x05')