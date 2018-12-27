# sound
import pygame as pg


class MySound:
	def __init__(self, audio, chan, vol, rep):
		self.audio = audio
		self.volume = vol
		self.channel = pg.mixer.Channel(chan)
		self.repeat = rep

	def play(self):
		self.channel.set_volume(self.volume)
		self.channel.play(self.audio, self.repeat)

	def stop(self):
		self.channel.stop()



freq = 44100
bitsize = -16
channels = 2
buffer = 2048
pg.mixer.init(freq, bitsize, channels, buffer)


#Sounds:
s_select = MySound			(pg.mixer.Sound('sounds/screenshot.wav'), 1, 0.4, 0)
s_select_cm = MySound		(pg.mixer.Sound('sounds/C#_AMBIENT.wav'), 2, 0.5, -1)
s_move = MySound			(pg.mixer.Sound('sounds/trap kick.wav'), 3, 0.5, 0)
s_rain = MySound			(pg.mixer.Sound('sounds/rain.wav'), 4, 0.4, -1)
s_win = MySound				(pg.mixer.Sound('sounds/wave_racer_impact.wav'), 5, 0.4, 0)

s_rain.play()
		


