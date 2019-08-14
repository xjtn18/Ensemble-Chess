import chess_model
from copy import deepcopy
from PIL.ImageTk import PhotoImage
from PIL import Image


white = 0
black = 1


"""
All pieces:
	valid_placements method returns a list of tuples containing positions in the 2D array
	display method gets passed the_canvas and draw whatever is stored in self._image
"""


def temp_all(board, color) -> list:
	""""returns a list of all placements"""
	res = set()
	for col in range(8):
		for row in range(8):
			spot = board[col][row]
			if spot and spot.color == (color + 1) % 2:
				for tup in spot.valid_placements(col, row, board, False):
					res.add(tup)
	return res


def filter_suicide(placements, col, row, board, color):
	for tup in placements:
		ncol,nrow = tup  # unpack the placement

		# move the piece on the potential board copy
		potential_board = deepcopy(board)
		potential_board[ncol][nrow] = potential_board[col][row]
		potential_board[col][row] = None


		if chess_model.ChessModel.KING_POSITIONS[color] in temp_all(potential_board, color):
			placements.remove(tup)

	return placements





class Pawn:

	def __init__(self, color):
		self.color = color
		image = Image.open(f'piece_images/pawn_{get_piece_color(color)}.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self._image = PhotoImage(image)

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

		if look_ahead:
			placements = filter_suicide(placements, col, row, board, self.color)
		return placements


	def display(self,x,y, the_canvas):
		the_canvas.create_image(x,y, image=self._image)
	
	def __deepcopy__(self, memo):
		return Pawn(deepcopy(self.color, memo))




class Rook:

	def __init__(self, color):
		self.color = color


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

	def __init__(self, color):
		self.color = color


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

	def __init__(self, color):
		self.color = color


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

	def __init__(self, color):
		self.color = color


	def valid_placements(self, col, row, board, look_ahead = True):
		placements = Rook.valid_placements(self, col, row, board) + Bishop.valid_placements(self, col, row, board)
		
		if look_ahead:
			placements = filter_suicide(placements, col, row, board, self.color)
		return placements





class King(Queen):

	def __init__(self, color):
		self.color = color


	def valid_placements(self, col, row, board, look_ahead = True):
		placements = Queen.valid_placements(self, col, row, board)
		placements = filter(lambda spot: -1 <= spot[0] - col <= 1 and -1 <= spot[1] - row <= 1, placements)
		
		if look_ahead:
			placements = filter_suicide(placements, col, row, board, self.color)
		return placements


def get_piece_color(color):
	"""returns the string white or black instead of the tkinter color name normally stored"""
	if color is white:
		return 'white'
	else:
		return 'black'


