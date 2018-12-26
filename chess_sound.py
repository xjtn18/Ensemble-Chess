# sound
import pygame as pg

#Channels
select_atmos = 3
move_kick = 2
rain = 1

class MySound:
	def __init__(self):
		freq = 44100
		bitsize = -16
		channels = 8
		buffer = 2048
		pg.mixer.init(freq, bitsize, channels, buffer)
		pg.mixer.music.load('sounds/rain.wav')
		pg.mixer.music.play(-1)
		pg.mixer.music.set_volume(0.1)


	def play(self, filename, ch, repeat=False):
		sound = pg.mixer.Sound(filename)
		chan = pg.mixer.Channel(ch)
		chan.set_volume(0.2)
		chan.play(sound) if not repeat \
			else chan.play(sound,-1)

	def stop(self, ch):
		pg.mixer.Channel(ch).stop()


my_sound = MySound()

