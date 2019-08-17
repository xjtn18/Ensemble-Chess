from chess_pieces import *
from math import floor
from chess_sound import *




class ChessModel:

	KING_POSITIONS = [(4,0), (4,7)]
	WINNER = None

	def __init__(self):
		self.current_player = white

		self.board = self.create_board()
		self.selection = None # stores a tuple of the array position of the selected piece
		self.selection_placements = ((-1,-1),)
		self.destination = None	# stores a tuple of the array position of the destination


		self.en_passant_active = False
		# Check Booleans
		self.white_in_check = False
		self.black_in_check = False


		# Castling Booleans - Perhaps these booleans update every turn using a helper function?
		self.white_king_castle = True # Can white castle King Side (O-O)?
		self.white_queen_castle = True # Can white castle Queen Side (O-O-O)?

		self.black_king_castle = True # Can black castle King Side (O-O)?
		self.black_queen_castle = True # Can black castle Queen Side (O-O-O)?




	def create_board(self):
		"""Returns a 2D array where None is an empty square and occupied squares
		hold chess piece objects."""
		board = [[None]*8 for i in range(8)]

		for i in range(8):
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

		captured = self.board[dcol][drow]
		if captured != None:
			play_capture_sound()

		self.board[dcol][drow] = self.board[scol][srow] # moves selected to destination
		self.board[scol][srow] = None # removes where the piece previously was


		# POST MOVE ANALYSIS #
		moved_piece = self.board[dcol][drow]
		if type(moved_piece) is King:
			self.update_king_pos(self.destination, self.current_player)

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


		opponent = self.opp()
		if in_check(self.board, opponent, ChessModel.KING_POSITIONS[opponent]):
			exec(f'self.{get_piece_color(opponent)}_in_check = True')
			if self.check_for_mate(opponent) == True:
				self.game_over()

		self.selection, self.destination = None, None

		self.current_player = self.opp()  # switch current player

		# END OF THE PLAY #


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




	def get_king_pos(self, color: int):
		return ChessModel.KING_POSITIONS[color]


	def update_king_pos(self, dest, color: int):
		ChessModel.KING_POSITIONS[color] = dest



	def opp(self):
		"""returns opponents color"""
		return (self.current_player + 1) % 2


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


	def reset_hints(self):
		self.selection_placements = ((-1,-1),)



	def game_over(self):
		"""Sets winner equal to whoever took a checkmated"""
		ChessModel.WINNER = self.current_player
		s_win.play()


