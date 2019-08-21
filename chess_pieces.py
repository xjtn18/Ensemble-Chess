import chess_model
from copy import deepcopy


white = 0
black = 1

right = 1
left = -1


"""
All pieces:
	valid_placements method returns a list of tuples containing positions in the 2D array
	display method gets passed the_canvas and draw whatever is stored in self._image
"""


def in_check(board, color, king_pos) -> bool:
	for col in range(8):
		for row in range(8):
			spot = board[col][row]
			if spot and spot.color != color: # only check pieces of opponent
				for tup in spot.valid_placements(col, row, board, False):
					if tup == king_pos:
						return True
	return False


def filter_suicide(placements, col, row, board, color):
	potential_board = deepcopy(board)
	removals = []
	for tup in placements:
		ncol,nrow = tup  # unpack the placement

		# move the piece on the potential board copy

		precessor = potential_board[ncol][nrow]
		potential_board[ncol][nrow] = potential_board[col][row]
		potential_board[col][row] = None

		if type(board[col][row]) is King:
			king_pos = (ncol,nrow)
		else:
			king_pos = chess_model.ChessModel.KING_POSITIONS[color]

		if in_check(potential_board, color, king_pos):
			removals.append(tup)

		potential_board[col][row] = potential_board[ncol][nrow]
		potential_board[ncol][nrow] = precessor

	for r in removals:
		placements.remove(r)

	return placements

def on_canvas_pos(current):
	sh = chess_model.ChessModel.sh
	w = chess_model.ChessModel.w
	return (current[0]*sh + sh/2 - 2, w - (current[1]*sh + sh/2))




class Pawn:

	def __init__(self, color, current):
		self.color = color
		self.en_passant = 0
		self.moved = False
		self.location = on_canvas_pos(current)


	def valid_placements(self, col, row, board, look_ahead = True):
		placements = []

		forward = 1
		if self.color == black:
			forward = -1
		times = 1
		if row == 1 or row == 6:
			times = 2


		nrow = row + forward
		if 0 <= col + 1 <= 7 and board[col + 1][nrow] != None and board[col + 1][nrow].color != self.color:
			placements.append((col + 1, nrow))
		if 0 <= col - 1 <= 7 and board[col - 1][nrow] != None and board[col - 1][nrow].color != self.color:
			placements.append((col - 1, nrow))
		for i in range(times):
			if 0 <= nrow <= 7:
				if board[col][nrow] == None:
					placements.append((col, nrow))
					nrow = nrow + forward
				else: break


		if self.en_passant != 0:
			if self.color == black:
				placements.append((col - self.en_passant, row - 1))
			else:
				placements.append((col - self.en_passant, row + 1))

		if look_ahead:
			placements = filter_suicide(placements, col, row, board, self.color)

		
		return placements





class Rook:

	def __init__(self, color, current):
		self.color = color
		self.location = on_canvas_pos(current)
		self.moved = False

	def valid_placements(self, col, row, board, look_ahead = True):
		placements = []
		for d in [(-1,0),(0,1),(1,0),(0,-1)]:
			ncol,nrow = col + d[0], row + d[1]
			while True:
				if 0 <= nrow <= 7 and 0 <= ncol <= 7:
					spot = board[ncol][nrow]
					if spot and spot.color == self.color:
						break
					elif spot:
						placements.append((ncol, nrow))
						break
					placements.append((ncol, nrow))
					ncol,nrow = ncol + d[0], nrow + d[1]
				else:
					break
		
		if look_ahead:
			placements = filter_suicide(placements, col, row, board, self.color)
		return placements





class Bishop:

	def __init__(self, color, current):
		self.color = color
		self.location = on_canvas_pos(current)
		self.moved = False


	def valid_placements(self, col, row, board, look_ahead = True):
		placements = []
		for d in [(-1,-1),(-1,1),(1,1),(1,-1)]:
			ncol,nrow = col + d[0], row + d[1]
			while True:
				if 0 <= nrow <= 7 and 0 <= ncol <= 7:
					
					spot = board[ncol][nrow]
					if spot and spot.color == self.color:
						break
					elif spot:
						placements.append((ncol, nrow))
						break
					placements.append((ncol, nrow))
					ncol,nrow = ncol + d[0], nrow + d[1]

				else:
					break
		
		if look_ahead:
			placements = filter_suicide(placements, col, row, board, self.color)
		return placements





class Knight:

	def __init__(self, color, current):
		self.color = color
		self.location = on_canvas_pos(current)
		self.moved = False

	def valid_placements(self, col, row, board, look_ahead = True):
		placements = []
		for d in [(-2,-1),(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2)]:
			ncol,nrow = col + d[0], row + d[1]
			if 0 <= nrow <= 7 and 0 <= ncol <= 7:

				spot = board[ncol][nrow]
				if spot and spot.color == self.color:
					continue
				placements.append((ncol, nrow))
		
		if look_ahead:
			placements = filter_suicide(placements, col, row, board, self.color)
		return placements





class Queen(Rook, Bishop):

	def __init__(self, color, current):
		self.color = color
		self.location = on_canvas_pos(current)
		self.moved = False

	def valid_placements(self, col, row, board, look_ahead = True):
		placements = Rook.valid_placements(self, col, row, board, False) + Bishop.valid_placements(self, col, row, board, False)
		
		if look_ahead:
			placements = filter_suicide(placements, col, row, board, self.color)
		return placements





class King(Queen):

	def __init__(self, color, current):
		self.color = color
		self.location = on_canvas_pos(current)
		self.moved = False
		self.castled = False

	def valid_placements(self, col, row, board, look_ahead = True):
		placements = Queen.valid_placements(self, col, row, board, False)
		placements = list(filter(lambda spot: -1 <= spot[0] - col <= 1 and -1 <= spot[1] - row <= 1, placements))
		
		if look_ahead:
			placements.extend(self.add_castle(col, row, board))
			placements = filter_suicide(placements, col, row, board, self.color)

		return placements


	def add_castle(self, col, row, board):
		res = set()
		if not self.moved and not in_check(board, self.color, (col,row)):
			rook1 =  board[col+3][row]
			middle = {(col+1, row), (col+2, row)}
			if not rook1.moved and self.middle_empty(middle, board) and not middle.issubset(chess_model.ChessModel.all_victims(board, self.color)):
				res.add((col+2, row))

			rook2 = board[col-4][row]
			middle = {(col-1, row), (col-2, row)}
			if not rook1.moved and self.middle_empty(middle, board) and not middle.issubset(chess_model.ChessModel.all_victims(board, self.color)):
				res.add((col-2, row))

		return res

	def middle_empty(self, middle, board):
		for spot in middle:
			col,row = spot
			if board[col][row] != None:
				return False
		return True




def get_piece_color(color):
	"""returns the string white or black instead of the tkinter color name normally stored"""
	if color is white:
		return 'white'
	else:
		return 'black'


