from chess_pieces import *
from math import floor
from chess_sound import *

class ChessModel:

	def __init__(self):
		self.current_player = white
		self.winner = None

		self.board = self.create_board()
		self.selection = None # stores a tuple of the array position of the selected piece
		self.destination = None	# stores a tuple of the array position of the destination

		# Update Booleans -
		self.white_in_check = False
		self.black_in_check = False

		# Castling Booleans - Perhaps these booleans update every turn using a helper function?
		self.white_king_castle = True # Can white castle King Side (O-O)?
		self.black_king_castle = True # Can white castle Queen Side (O-O-O)?

		self.black_king_castle = True # Can black castle King Side (O-O)?
		self.black_queen_castle = True # Can black castle Queen Side (O-O-O)?

		#random comment

	def create_board(self):
		"""Returns a 2D array where None is an empty square and occupied squares
		hold chess piece objects."""
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
		"""Takes selected and destination and moves the piece to the destination"""
		scol,srow = self.selection
		dcol,drow = self.destination

		self.check_game_over(dcol, drow)

		self.board[dcol][drow] = self.board[scol][srow] # moves selected to destination
		self.board[scol][srow] = None # removes where the piece previously was

		self.selection, self.destination = None, None
		self.change_current_move()

	def squareUnderAttack(x: int, y: int,) -> bool:
		'''
		Returns whether or not, in the current board state, a square is currently
		under attack (aka the Opponent could take a piece on that square next turn)
		'''


	def change_current_move(self):
		"""Switches the turn after a play has been made"""
		if self.current_player == white:
			self.current_player = black
		else:
			self.current_player = white


	def mouse_click(self,x,y):
		"""Takes the mouse click coordinates and converts it to a position in the
		2D array. Changes selected piece and calls update if valid destination is clicked."""
		square = (floor((x)/75),floor((600-y)/75)) # hard coded based on canvas size
		col, row = square

		# Prevents wierd cases where pressing the edge of the canvas creates indexes
			# not in the array.
		if 0 <= col <= 7 and 0 <= row <= 7:
			clicked = self.board[col][row]
		else:
			return


		if self.selection:	# if a piece has been selected
			scol, srow = self.selection
			selected = self.board[scol][srow]

			if square == self.selection:	# If clicked square is same as selected, remove selection
				self.selection = None
			else:	# clicked square is not the already selected one
				if clicked and clicked.color == self.current_player:	# clicked square is just another selection
					self.selection = square
					s_select_cm.stop()
					s_select.play()

				elif square in selected.valid_placements(scol, srow, self.board): # clicked square is a valid placement
					self.destination = (col,row)
					s_select_cm.stop()
					s_move.play()
					self.update() # move the piece to the destination

				else: # clicked square
					pass
					# play error sound

		elif clicked and clicked.color == self.current_player: # if there is no selected piece and clicked is a current players piece
			self.selection = square
			s_select.play()

		self.check_for_mate() # after making a selection, check if the other players king is in position



	def check_for_mate(self):
		"""Checks if the other players king is in valid placements of selected."""
		if self.selection:
			scol,srow = self.selection
			for dcol,drow in self.board[scol][srow].valid_placements(scol,srow, self.board):
				if type(self.board[dcol][drow]) is King:
					s_select_cm.play()
		else:
			s_select_cm.stop()



	def check_game_over(self, dcol, drow):
		"""If destination was a king, end game"""
		if type(self.board[dcol][drow]) is King:
			self.game_over()



	def game_over(self):
		"""Sets winner equal to whoever took a King"""
		self.winner = self.current_player
		#s_win.play()
