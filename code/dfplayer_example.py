
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

from time import sleep

music = Player(pin_TX=machine.Pin(0), pin_RX=machine.Pin(1))
sleep(0.1) #await init process
music.module_wake()
sleep(0.1)
print("set volume")
music.volume(80) #setting volume in percent

print("start play")
music.play(1) #play track 1 of root directory
sleep(5)
music.stop() #stop track

music.play('next')
sleep(5)
music.pause()
sleep(2)
music.resume()
sleep(3)
music.stop()

music.play(1, 2) #play 1. track in folder 2
sleep(10)
music.stop()

music.module_sleep()