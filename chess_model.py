from chess_pieces import *
from math import floor
from chess_sound import *
from fractions import gcd
import sys
import time
import math

TRANSITION_RATE = 35

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
			scol, srow = self.selection

			if square == self.selection:	# If clicked square is same as selected, remove selection
				self.selection = None
				self.reset_hints()
				#play_select_sound() # play a subtke non tonal sound here
				return

			else:	# clicked square is not the already selected one
				if clicked and clicked.color == self.current_player:	# clicked square is just another selection
					self.selection = square
					scol, srow = self.selection
					self.selection_placements = self.board[scol][srow].valid_placements(scol, srow, self.board)
					play_select_sound()


				######## MOVE MADE ##########
				elif square in self.selection_placements: # clicked square is a valid placement
					self.destination = (col,row)
					self.reset_hints()
					play_move_sound(self.board[scol][srow])
					self.update() # move the piece to the destination
					##########


				else: # clicked square
					self.selection = None
					self.reset_hints()
					# play error sound

		elif clicked and clicked.color == self.current_player: # if there is no selected piece and clicked is a current players piece
			self.selection = square
			scol, srow = self.selection
			self.selection_placements = self.board[scol][srow].valid_placements(scol, srow, self.board)
			play_select_sound()




	def update(self):
		"""Takes selected and destination and moves the piece to the destination"""
		scol,srow = self.selection
		dcol,drow = self.destination

		captured = self.board[dcol][drow]


		# Transition piece

		self.board[scol][srow].moved = True
		self.transition(self.board[scol][srow], self.selection, self.destination)

		self.board[dcol][drow] = self.board[scol][srow] # moves selected to destination
		self.board[scol][srow] = None # removes where the piece previously was

		

					# POST MOVE ANALYSIS #


		moved_piece = self.board[dcol][drow]
		if type(moved_piece) is King:

			# Castling Check
			travel = scol - dcol
			print(travel)
			if abs(travel) > 1:
				if travel < 0: # top rook
					rcol, nrcol = 7, 5
				else: # bottom rook
					rcol, nrcol = 0, 3

				self.board[rcol][drow].moved = True
				self.transition(self.board[rcol][drow], (rcol,drow), (nrcol,drow))

				self.board[nrcol][drow] = self.board[rcol][drow] # moves selected to destination
				self.board[rcol][drow] = None # removes where the piece previously was

			# Update King Positions
			self.update_king_pos(self.destination, self.current_player)


		# Check En Passant
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
				self.board[dcol][drow - (drow - srow)] = None

		# Check Endgame
		opponent = self.opp()
		if in_check(self.board, opponent, ChessModel.KING_POSITIONS[opponent]):
			exec(f'self.{get_piece_color(opponent)}_in_check = True')
			if self.check_for_mate(opponent) == True:
				self.game_over()

		self.selection, self.destination = None, None

		self.current_player = self.opp()  # switch current player

		# END OF THE PLAY #




		# Transition Animation #


	def floor_tuple(self, tup):
		tup = ( floor(tup[0]), floor(tup[1]) )
		return tup

	def get_max_axis(self, point):
		x,y = point
		my_max = max(x,y)
		return my_max

	def distance(self, p1, p2):
		x1,y1 = p1
		x2,y2 = p2
		return math.sqrt((y2 - y1)**2 + (x2 - x1)**2)


	def calc_direction(self, start, end):
		s1,s2 = start
		e1,e2 = end
		a = e1-s1
		b = e2-s2
		a = 1 if a == 0 else a/abs(a)
		b = 1 if b == 0 else b/abs(b)
		return (a,b)


	def transition(self, piece, start, end):
		sh = ChessModel.sh
		w = ChessModel.w
		dcol, drow = end
		slope = self.get_slope(start, end)
		final = (dcol*sh + sh/2 - 2, w - (drow*sh + sh/2))
		sma = self.get_max_axis(slope)
		direction = self.calc_direction(piece.location, final)
		self.loop(piece, sma, final, slope, direction, TRANSITION_RATE)


	def loop(self, piece, sma, final, slope, direction, rate):
		for i in range(rate):
			distance = floor(self.distance(piece.location, final))
			if distance <= sma:
				play_capture_sound()
				piece.location = final

				return
			self.move(piece, slope, direction)
			#rate = floor(rate/(rate/5)/distance + 10)
		self.root.after(1, self.loop, piece, sma, final, slope, direction, rate)


	def get_slope(self, p1, p2):
		fract = (p1[1] - p2[1], p1[0] - p2[0])
		my_gcd = gcd(fract[0], fract[1])
		res = (fract[0]/my_gcd, fract[1]/my_gcd)
		return res


	def move(self, piece, slope, direction):
		p1,p2 = piece.location
		s1,s2 = slope
		s1 = abs(s1)
		d1,d2 = direction
		piece.location = (p1 + s2*d1, p2 + s1*d2)




		# Case Analysis #

	def clear_en_passant(self):
		"""as soon as we find a piece that has a valid move, we know its not check mate"""
		for col in range(8):
			for row in range(8):
				spot = self.board[col][row]
				if type(spot) is Pawn and spot.en_passant != 0:
					spot.en_passant = 0



	def check_for_mate(self, color):
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




