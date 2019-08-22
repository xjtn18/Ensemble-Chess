from chess_pieces import *
from chess_sound import *
import chess_view
from math import floor
from fractions import gcd
import sys
import time
import math

#CASTLING = 1
#EN_PASSANT = 2


class ChessModel:

	KING_POSITIONS = [(4,0), (4,7)]
	WINNER = None
	w = 606
	sh = 75.75

	def __init__(self, root):
		self.root = root
		self.current_player = white

		self.board = self.create_board()
		self.selection = None # stores a tuple of the array position of the selected piece
		self.selection_placements = ((-1,-1),)
		self.destination = None	# stores a tuple of the array position of the destination


		self.en_passant_active = False
		# Check Booleans
		self.white_in_check = False
		self.black_in_check = False

		self.moveType = 0



	def create_board(self):
		"""Returns a 2D array where None is an empty square and occupied squares
		hold chess piece objects."""
		board = [[None]*8 for i in range(8)]

		for i in range(8):
			board[i][1] = Pawn(white, (i,1))
			board[i][6] = Pawn(black, (i,6))

		board[0][0] = Rook(white, (0,0))
		board[1][0] = Knight(white, (1,0))
		board[2][0] = Bishop(white, (2,0))
		board[3][0] = Queen(white, (3,0))
		board[4][0] = King(white, (4,0))
		board[5][0] = Bishop(white, (5,0))
		board[6][0] = Knight(white, (6,0))
		board[7][0] = Rook(white, (7,0))

		board[0][7] = Rook(black, (0,7))
		board[1][7] = Knight(black, (1,7))
		board[2][7] = Bishop(black, (2,7))
		board[3][7] = Queen(black, (3,7))
		board[4][7] = King(black, (4,7))
		board[5][7] = Bishop(black, (5,7))
		board[6][7] = Knight(black, (6,7))
		board[7][7] = Rook(black, (7,7))

		return board



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


		if self.selection:	# if a piece has already been selected at the time of the click
			select = self.selection
			scol, srow = select

			if square == self.selection:	# If clicked square is same as selected, remove selection
				self.selection = None
				self.reset_hints()
				play_cancel()
				return

			else:	# clicked square is not the already selected one
				if clicked and clicked.color == self.current_player:	# clicked square is just another selection
					self.selection = square
					scol, srow = self.selection
					self.selection_placements = self.board[scol][srow].valid_placements(scol, srow, self.board)
					play_select()


				######## MOVE MADE ##########
				elif square in self.selection_placements: # clicked square is a valid placement
					self.destination = (col,row)
					self.reset_hints()
					#play_move(self.board[scol][srow])
					self.update() # move the piece to the destination
				############################


				else: # clicked square
					self.selection = None
					play_cancel()
					self.reset_hints()
					# play error sound

		elif clicked and clicked.color == self.current_player: # if there is no selected piece and clicked is a current players piece
			self.selection = square
			scol, srow = self.selection
			self.selection_placements = self.board[scol][srow].valid_placements(scol, srow, self.board)
			play_select()





	def update(self):
		"""Takes selected and destination and moves the piece to the destination"""
		scol,srow = self.selection
		dcol,drow = self.destination
		captured = self.board[dcol][drow]

		# Transition and Move piece
		self.move(self.selection, self.destination)

		moved_piece = self.board[dcol][drow]
		
		# POST MOVE ANALYSIS #
		self.check_double_step(moved_piece, srow, drow)
		self.check_castle()
		self.check_en_passant(captured)
		self.check_upgrade()
		self.check_end_game()

		play_move_sound(moved_piece, self.moveType)

		self.new_play()
		self.current_player = self.opp()  # switch current player

		# END OF THE PLAY #



	def new_play(self):
		self.selection, self.destination = None, None
		self.moveType = 0




	def move(self, selection, destination):
		scol, srow = selection
		dcol, drow = destination
		self.board[scol][srow].moved = True
		chess_view.ChessGame.transition(self.board[scol][srow], self.selection, self.destination, self.root)
		self.board[dcol][drow] = self.board[scol][srow] # moves selected to destination
		self.board[scol][srow] = None # removes where the piece previously was



	def check_upgrade(self):
		dcol,drow = self.destination
		piece = self.board[dcol][drow]

		if type(piece) is Pawn and drow in (0,7): # upgrade
			#self.root.after(2000, chess_view.ChessGame.wait_for_transition, piece, self.destination)
			if drow == 0: # black pawn
				#self.root(after(self.create_upgrade()
				self.delay(100, self.create_piece, black, self.destination)
			else: # white pawn
				self.delay(100, self.create_piece, white, self.destination)
			


	def delay(self, amt, function, *arg):
		self.root.after(amt, function, *arg)

	def create_piece(self, color, place):
		col, row = place
		self.board[col][row] = Queen(color, (col,row))
		self.board[col][row].moved = True


	def check_double_step(self, piece, srow, drow):
		if type(piece) is Pawn and abs(srow - drow) == 2:
			self.moveType = DOUBLE_STEP



	def check_castle(self):
		scol,srow = self.selection
		dcol,drow = self.destination
		moved_piece = self.board[dcol][drow]

		if type(moved_piece) is King:
			# Castling Check
			travel = scol - dcol
			if abs(travel) > 1:
				self.moveType = CASTLE
				print(self.moveType)
				if travel < 0: # rightside rook
					rcol, nrcol = 7, 5
				else:				 # leftside rook
					rcol, nrcol = 0, 3

				#self.move((rcol,drow), (nrcol,drow))

				self.board[rcol][drow].moved = True
				chess_view.ChessGame.transition(self.board[rcol][drow], (rcol,drow), (nrcol,drow), self.root)
				self.board[nrcol][drow] = self.board[rcol][drow]
				self.board[rcol][drow] = None

			# Update King Positions
			self.update_king_pos(self.destination, self.current_player)



	def check_en_passant(self, captured):
		scol,srow = self.selection
		dcol,drow = self.destination
		moved_piece = self.board[dcol][drow]

		if self.en_passant_active:
			self.en_passant_active = False
			self.clear_en_passant()

		if type(moved_piece) is Pawn:
			if abs(drow - srow) == 2:
				self.en_passant_active = True
				if dcol < 7 and type(self.board[dcol+1][drow]) is Pawn and self.board[dcol+1][drow].color != self.current_player:
					self.board[dcol+1][drow].en_passant = 1
				if dcol > 0 and type(self.board[dcol-1][drow]) is Pawn and self.board[dcol-1][drow].color != self.current_player:
					self.board[dcol-1][drow].en_passant = -1
			elif scol != dcol and captured == None:  # an en passant move was made
				self.moveType = EN_PASSANT
				self.board[dcol][drow - (drow - srow)] = None



	def check_end_game(self):
		opponent = self.opp()
		if in_check(self.board, opponent, ChessModel.KING_POSITIONS[opponent]):
			exec(f'self.{get_piece_color(opponent)}_in_check = True')
			if self.mate(opponent) == True:
				self.game_over()





	def clear_en_passant(self):
		for col in range(8):
			for row in range(8):
				spot = self.board[col][row]
				if type(spot) is Pawn and spot.en_passant != 0:
					spot.en_passant = 0



	def mate(self, color):
		"""as soon as we find a piece that has a valid move, we know its not check mate"""
		for col in range(8):
			for row in range(8):
				spot = self.board[col][row]
				if spot and spot.color == color:
					if spot.valid_placements(col, row, self.board) != []:
						return False
		return True




	# Helpers #

	def get_king_pos(self, color: int):
		return ChessModel.KING_POSITIONS[color]


	def update_king_pos(self, dest, color: int):
		ChessModel.KING_POSITIONS[color] = dest


	def opp(self):
		"""returns opponents color"""
		return (self.current_player + 1) % 2


	def reset_hints(self):
		self.selection_placements = ((-1,-1),)


	def game_over(self):
		"""Sets winner equal to whoever took a checkmated"""
		ChessModel.WINNER = self.current_player


	@staticmethod
	def all_victims(board, color) -> set:
		res = set()
		for col in range(8):
			for row in range(8):
				spot = board[col][row]
				if spot and spot.color == (color + 1) % 2:
					for tup in spot.valid_placements(col, row, board, False):
						res.add(tup)
		return res




