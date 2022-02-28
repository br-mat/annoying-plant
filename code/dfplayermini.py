import utime
from machine import UART, Timer

IDLE = 0
PAUSED = 1
PLAYING = 2


class Player:
    def __init__(self, pin_TX, pin_RX):
        self.uart = UART(0, 9600, tx=pin_TX, rx=pin_RX, bits=8, parity=None, stop=0)
        self.cmd(0x3F)  # send initialization parametres
        self._fadeout_timer = Timer(-1)

        self._volume = 15
        self._max_volume = 50
        self._fadeout_speed = 0


    def cmd(self, command, parameter=0, parameter2=0):
        query = bytes([0x7e, 0xFF, 0x06, command,
                       0x00, parameter2, parameter, 0xEF])
        print(query)
        self.uart.write(query)

    def _fade_out_process(self, timer):
        new_volume = self._volume - self._fadeout_speed
        
        if new_volume <= 0:
            print("fadeout finished")
            new_volume = 0
            self._fadeout_timer.deinit()
            self.stop()
            new_volume = self._max_volume # reset volume to max 
        self.volume(new_volume)

    # playback

    def play(self, track_id=False, folder=False):
        if not track_id:
            self.resume()
        elif folder:
            print(f'Go folder {folder}')
            if isinstance(track_id, int) and isinstance(folder, int):
                print(f'play {track_id}')
                #self.cmd(0x0F, parameter=0x00, parameter2=folder)
                self.cmd(0x0F, track_id, folder)
        elif isinstance(track_id, int):
            self.cmd(0x03, track_id)
            print(f'play {track_id}')
            
    def pause(self):
        self.cmd(0x0E)

    def resume(self):
        self.cmd(0x0D)

    def stop(self):
        self.cmd(0x16)

    def fadeout(self, fadeout_ms=1000):
        # more than 500ms and less than 3000ms
        fadeout_ms = int(sorted([500, fadeout_ms, 3000])[1])
        fade_out_step_ms = 100
        self._fadeout_speed = self._volume * \
            fade_out_step_ms / fadeout_ms  # ten steps per second
        self._fadeout_timer.init(
            period=fade_out_step_ms, callback=self._fade_out_process)

    def loop_track(self, track_id):
        self.cmd(0x08, track_id)

    def loop(self):
        self.cmd(0x19)

    def loop_disable(self):
        self.cmd(0x19, 0x01)

    # volume control

    def volume_up(self):
        self._volume += 1
        self.cmd(0x04)

    def volume_down(self):
        self._volume -= 1
        self.cmd(0x05)

    def volume(self, volume=False):
        if volume:
            self._volume = int(sorted([0, volume, self._max_volume])[1])
            print("volume", self._volume)
            self.cmd(0x06, self._volume)
        
        return self._volume

    # hardware

    def module_sleep(self):
        self.cmd(0x0A)

    def module_wake(self):
        self.cmd(0x0B)

    def module_reset(self):
        self.cmd(0x0C)

