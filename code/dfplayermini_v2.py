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

import utime
from machine import UART, Timer






class Player:
#########################################################################
# constructor
#########################################################################
    def __init__(self, pin_TX, pin_RX):
        self.uart = UART(0, 9600, tx=pin_TX, rx=pin_RX, bits=8, parity=None, stop=0)
        self.cmd(0x3F)  # send initialization parametres
        self._fadeout_timer = Timer(-1)

        self._volume = 100
        self._max_volume = 30
        self._fadeout_speed = 0

        utime.sleep_ms(100) #await init

        self.volume(50) #initialize volume at 50%

#########################################################################
# methods
#########################################################################
    def cmd(self, command, parameter=0, parameter2=0):
        query = bytes([0x7e, 0xFF, 0x06, command,
                       0x00, parameter2, parameter, 0xEF])
        #print(query)
        self.uart.write(query)
        utime.sleep_ms(600 if command == 0x0C else 50)

    def play(self, track_id=False, folder=False):
        if folder:
            if not isinstance(folder, int): #ignore folder on incorrect input
                print("Warning: folder type not correct")
                folder=False
        if track_id:
            if not isinstance(track_id, int): #play track 1 on incorrect input
                print("Warning: track_id type not correct")
                track_id=1

        if folder:
            print(f'Go folder {folder} play {track_id}')
            self.cmd(0x0F, track_id, folder)
        elif track_id:
            self.cmd(0x03, track_id)
            print(f'play {track_id}')
        else:
            self.resume()
            
    def pause(self):
        self.cmd(0x0E)

    def resume(self):
        self.cmd(0x0D)

    def stop(self):
        self.cmd(0x16)

    def loop_track(self, track_id):
        self.cmd(0x08, track_id)

    def loop(self):
        self.cmd(0x19)

    def loop_disable(self):
        self.cmd(0x19, 0x01)

    def volume_up(self):
        self._volume += 1
        self.cmd(0x04)

    def volume_down(self):
        self._volume -= 1
        self.cmd(0x05)

    def volume(self, vol_percent):
        if not isinstance(vol_percent, int):
            vol_percent=0
        perc = int(sorted([0, vol_percent, 100])[1]) #between 0 and 100
        self._volume = int(perc*self._max_volume/100)
        self.cmd(0x06, self._volume)
        print(f"set volume {self._volume} ({perc}%)")
        return self._volume

    def module_sleep(self):
        self.cmd(0x0A)

    def module_wake(self):
        self.cmd(0x0B)

    def module_reset(self):
        self.cmd(0x0C)