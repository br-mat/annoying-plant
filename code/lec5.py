from ds3231_impl import ds3231
import time

I2C_PORT = 0
I2C_SDA = 16
I2C_SCL = 17

rtc = ds3231(I2C_PORT,I2C_SCL,I2C_SDA) #init serial communication with RTC module
time.sleep_ms(50) #give init process some time
rtc.set_time('13:26:25,Tuesday,2022-03-22') #set rtc time uncomment if needed
time.sleep_ms(1)

while 1:
    print(rtc.read_time()) #read time and print it
    time.sleep(5) #sleep 5 seconds