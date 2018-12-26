from chess_pieces import *
from math import floor
from chess_sound import *

# Global
global white,black
CURRENT_PLAYER = white

class ChessModel:

	def __init__(self):
		self.board = self.create_board()
		self.selection = None
		self.destination = None
		self.winner = None

	def create_board(self):
		global white, black
		board = [[None]*8 for i in range(8)]

		for i in range(8):
			pass
			board[i][1] = Pawn(white)
			board[i][6] = Pawn(black)

		board[0][0] = Rook(white)
		board[1][0] = Knight(white)
		board[2][0] = Bishop(white)
		board[3][0] = Queen(white)
		board[4][0] = King(white)
		board[5][0] = Bishop(white)
		board[6][0] = Knight(white)
		board[7][0] = Rook(white)

		board[0][7] = Rook(black)
		board[1][7] = Knight(black)
		board[2][7] = Bishop(black)
		board[3][7] = Queen(black)
		board[4][7] = King(black)
		board[5][7] = Bishop(black)
		board[6][7] = Knight(black)
		board[7][7] = Rook(black)

		return board


	def update(self):
		scol,srow = self.selection
		dcol,drow = self.destination
		if type(self.board[dcol][drow]) is King:
			self.game_over()
			return

		self.board[dcol][drow] = self.board[scol][srow] 
		self.board[scol][srow] = None

		self.selection, self.destination = None, None
		self.change_current_move()

		#self.check_game_over()


	def change_current_move(self):
		global white, black, CURRENT_PLAYER
		if CURRENT_PLAYER == white:
			CURRENT_PLAYER = black
		else:
			CURRENT_PLAYER = white
		my_sound.play('sounds/trap kick.wav', move_kick)


	def mouse_click(self,x,y):
		global CURRENT_PLAYER
		square = (floor(x/75),floor((600-y)/75))
		#print(square)
		col, row = square
		try:
			clicked = self.board[col][row]
		except IndexError:
			return


		if self.selection != None:
			scol, srow = self.selection
			selected = self.board[scol][srow]
			if square == self.selection:
				self.selection = None
				my_sound.stop(select_atmos)
			else:
				if clicked != None and clicked.color == CURRENT_PLAYER:
					self.selection = square
					my_sound.stop(select_atmos)
					my_sound.play('sounds/C#_AMBIENT.wav', select_atmos, repeat=True)
				elif square in selected.valid_placements(scol, srow, self.board):
					self.destination = (col,row)
					my_sound.stop(select_atmos)
					self.update()
				else:
					pass
					# play error sound
		elif clicked != None and clicked.color == CURRENT_PLAYER:
			self.selection = square
			my_sound.play('sounds/C#_AMBIENT.wav', select_atmos, repeat=True)


	def game_over(self):
		global CURRENT_PLAYER
		self.winner = CURRENT_PLAYER


