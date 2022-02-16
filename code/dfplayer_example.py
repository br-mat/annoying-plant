from dfplayermini import Player

from time import sleep

music = Player(pin_TX=machine.Pin(0), pin_RX=machine.Pin(1))
music.module_wake()
sleep(1)
print("set volume")
music.volume(50)

print("start play")
music.play(1)
music.volume(30)
sleep(10)

print("stop play with fadeout")
music.fadeout(5000)
sleep(5)
music.play('next')
sleep(10)

music.pause()
sleep(3)

music.loop()
music.play(2)
sleep(20)

music.module_sleep()