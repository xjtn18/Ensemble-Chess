# sound
import pygame as pg
from chess_pieces import Pawn, Knight, Rook, Bishop, Queen, King


class MySound:
	"""Stores all pygame mixer sound objects"""
	
	sps = 0  # tracks section of selection sound pattern
	
	def __init__(self, audio, chan, vol, rep):
		self.audio = audio
		self.volume = vol
		self.channel = pg.mixer.Channel(chan)
		self.repeat = rep

	def play(self):
		"""Plays each sound on their specified channel"""
		self.channel.set_volume(self.volume)
		self.channel.play(self.audio, self.repeat)

	def stop(self):
		self.channel.stop()


# Initialize pygame mixer
freq = 44100
bitsize = -16
channels = 2
buffer = 2048
pg.mixer.init(freq, bitsize, channels, buffer)


#All Sounds
s_rain = MySound(pg.mixer.Sound('sounds/rain.wav'), 1, 0.3, -1)
s_amb = MySound(pg.mixer.Sound('sounds/amb.wav'), 2, 0.8, -1)

s_beat = MySound(pg.mixer.Sound('sounds/beat.wav'), 3, 1, -1)
s_heart = MySound(pg.mixer.Sound('sounds/heart.wav'), 4, 1, 0)

s_bell = MySound(pg.mixer.Sound('sounds/bell.wav'), 5, 1, 0)

# Piece move sounds
s_pawn_move = MySound(pg.mixer.Sound('sounds/pawn_move.wav'), 6, 1, 0)
s_knight_move = MySound(pg.mixer.Sound('sounds/knight_move.wav'), 6, 1, 0)
s_queen_move = MySound(pg.mixer.Sound('sounds/queen_move.wav'), 6, 1, 0)
s_queen_power_move = MySound(pg.mixer.Sound('sounds/queen_power_move.wav'), 6, 1, 0)
s_bishop_move = MySound(pg.mixer.Sound('sounds/bishop_move.wav'), 6, 1, 0)
s_pawn_2_move = MySound(pg.mixer.Sound('sounds/pawn_2_move.wav'), 6, 1, 0)
s_en_passant_move = MySound(pg.mixer.Sound('sounds/en_passant_move.wav'), 6, 1, 0)

s_attack = MySound(pg.mixer.Sound('sounds/attack.wav'), 7, 1, 0)



#s_rain.play()
s_amb.play()
s_beat.play()


def play_select_sound():
	s_heart.play()

def play_capture_sound():
	s_attack.play()

def play_move_sound(piece):
	if type(piece) is Pawn:
		s_pawn_move.play() if not piece.en_passant else s_en_passant_move.play()
	elif type(piece) is Knight:
		s_knight_move.play()
	elif type(piece) is Bishop:
		s_bishop_move.play()
	elif type(piece) is Queen:
		s_queen_power_move.play()

	#exec(f's_p{MySound.sps + 1}.play()')
	MySound.sps = (MySound.sps + 1) % 4



