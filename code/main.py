#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a script that has not been tested and comes with no warranty. Use at your own risk.
# However, it is based on a basic version of the script which has been tested.
# The script has also been optimized using ChatGPT, it contributed to most of the documentation and description for the script.
# Additionally it provided help with the improved functions for mean and median values

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

# Constants, this constants should be able to controll the whole process

# Define pins
I2C_PORT = 0
I2C_SDA = 16
I2C_SCL = 17

analog_value=ADC(28)

ALARM_PIN = 14

led = Pin(25, Pin.OUT)
reset = Pin(20, Pin.OUT)

# Define baseline
dry_baseline = 600


# Set up sound dict
sounds={'music': [1, 2], 'voicline_thirsty_aut': [2, 16], 'voiceline_random_aut': [3, 22]} # dictionary containing lists [folder, num tracks]

# Set the verbosity level (higher values mean more frequent audio messages)
verbosity_level = 3

# Set the time ranges for the plant to be active
active_times = [
    [12, 0, 15, 0], # 12:00 - 15:00
    [18, 0, 22, 0]  # 18:00 - 22:00
]

def pick_random_track(content_list):
    """
    Plays a random audio track from a specified folder on a DFPlayer Mini module.
    Parameters:
    - content_list: a list containing the folder number and the number of tracks in the folder. The list should be formatted as [folder_number, num_tracks].
    Returns:
    - None
    """
    # Select a random track number from the specified range
    number = random.randint(1, content_list[1])
    
    # Initialize the DFPlayer Mini module and set the volume to 25
    music = Player(pin_TX=machine.Pin(0), pin_RX=machine.Pin(1))
    time.sleep_ms(10)
    music.volume(25)
    time.sleep_ms(10)
    
    # Play the selected track in the specified folder
    music.play(number, content_list[0])
    
    # Wait for the track to finish playing (optimized?)
    #while music.is_playing():
    #    time.sleep(0.1)
    
    # Wait for 12 seconds and stop playback
    time.sleep(12)
    music.stop()

def adc_median(adc, num_readings=100):
    """
    Takes a series of readings from an ADC and returns the median value.
    Parameters:
    - adc: an instance of the ADC object to be used to take the readings
    - num_readings: an optional integer specifying the number of readings to take. The default value is 500.
    Returns:
    - The median value of the readings as an integer.
    """
    vals = [0] * num_readings  # Initialize a list to store the readings
    for index, element in enumerate(vals):
        vals[index] = adc.read_u16()  # Take a reading from the ADC and store it in the list
    return sorted(vals)[num_readings // 2]  # Sort the list and return the middle value as the median

def adc_median_quickselect(adc, num_readings=1000):
    """
    More efficient implementation, for larger lists (hopefully)
    Takes a series of readings from an ADC and returns the median value.
    Parameters:
    - adc: an instance of the ADC object to be used to take the readings
    - num_readings: an optional integer specifying the number of readings to take. The default value is 500.
    Returns:
    - The median value of the readings as an integer.
    """
    vals = [0] * num_readings  # Initialize a list to store the readings
    for index, element in enumerate(vals):
        vals[index] = adc.read_u16()  # Take a reading from the ADC and store it in the list
        
    def quickselect(arr, k):
        """
        Finds the kth smallest element in arr using the quickselect algorithm.
        Parameters:
        - arr: a list of integers
        - k: an integer specifying the position of the element to be found
        Returns:
        - The kth smallest element in arr
        """
        if not arr:
            return None
        pivot = random.choice(arr)
        left = [x for x in arr if x < pivot]
        right = [x for x in arr if x > pivot]
        equal = [x for x in arr if x == pivot]
        if k < len(left):
            return quickselect(left, k)
        elif k < len(left) + len(equal):
            return equal[0]
        else:
            return quickselect(right, k - len(left) - len(equal))
    
    return quickselect(vals, num_readings // 2)


def adc_mean(adc, num_readings=100):
    """
    Takes a series of readings from an ADC and returns the mean value.
    Parameters:
    - adc: an instance of the ADC object to be used to take the readings
    - num_readings: an optional integer specifying the number of readings to take. The default value is 500.
    Returns:
    - The mean value of the readings.
    """
    vals = [0] * num_readings  # Initialize a list to store the readings
    for index, element in enumerate(vals):
        vals[index] = adc.read_u16()  # Take a reading from the ADC and store it in the list
    mean = sum(vals) / len(vals)  # Calculate the mean value of the readings
    return mean

def adc_mean_effivient(adc, num_readings=1000):
    """
    This should be a more efficient implementation for larger arrays
    Takes a series of readings from an ADC and returns the mean value.
    Parameters:
    - adc: an instance of the ADC object to be used to take the readings
    - num_readings: an optional integer specifying the number of readings to take. The default value is 500.
    Returns:
    - The mean value of the readings.
    """
    mean = 0  # Initialize the mean value to 0
    for i in range(num_readings):
        # Take a reading from the ADC
        reading = adc.read_u16()
        
        # Update the mean value incrementally using the formula:
        # mean = mean + (reading - mean) / (i + 1)
        mean += (reading - mean) / (i + 1)
        
    return mean

    
    
if __name__ == '__main__':
    time.sleep_ms(50) #give init process some time
    led.value(0) # activate onboard LED
    rtc = ds3231(I2C_PORT,I2C_SCL,I2C_SDA) #init serial communication with RTC module
    time.sleep_ms(50) #give init process some time
    
    # Read the status register
    status = rtc.read_status()

    # Check if the alarm flag is set and reset it
    try:
        # Check if an alarm has been triggered
        if rtc.alarm_triggered():
            # Clear the alarm flag
            rtc.clear_alarm_flag()
    except Exception as e:
        # Print an error message if there was a problem communicating with the DS3231
        print("Error:", e)
    
    #rtc.set_time('13:26:25,Tuesday,2022-02-17') #set rtc time uncomment if needed
    #time.sleep_ms(1)

    # Read the current time from the RTC module
    y, month, day, h, min1, sec1, wday = rtc.read_time()
    
    # Check if the current time is within one of the active time ranges
    for time_range in active_times:
        start_hour, start_minute, end_hour, end_minute = time_range
        if start_hour <= h < end_hour or (h == end_hour and min1 < end_minute):
            # Current time is within an active time range
            
            # Clamp verbosity between 0 and 5
            verbosity_level = max(0, min(5, verbosity_level))
            
            # Generate a random number between 0 and 1
            random_value = random.random()
            
            # Calculate the quadratic threshold based on the verbosity level
            # (higher values mean more frequent audio messages)
            threshold_dry = random_value > (verbosity_level / 5) ** 2
            
            threshold_moist = random_value > ((verbosity_level / 5) ** 2) ** 2
            
            # Check for action
            if not (threshold_dry or threshold_moist):
                break
            
            # Take analog read with a given function, to get ridd of unstable measurements we use:
            # median will take the value which is exact in the mid of a sorted list of readings
            # mean will take the mean value of this list of readings
            a_read = adc_median(analog_read, num_readings=1000)
            
            # Possible way to improve: add an upper baseline indicating that the plant got too moist
            if _low <= a_read <= _up: #check for reasonable values
                if a_read > dry_baseline: #check if plant is dry
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
        
        # Put the controller into deep sleep by cutting off its power supply
        # Set the alarm mode to once per minute
        alarm_mode = ds3231_impl.ALARM_MODE_MINUTE
        
        # Set next alarm
        rtc.set_alarm1(alarm_type, alarm_time, alarm_mode)
        
        time.sleep_ms(50)
        
        #reset FF and shutdown pico's supply
        print('shutdown')
        led.value(0)
        time.sleep_ms(50)
        reset.value(1)