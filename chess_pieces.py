import chess_model
from PIL.ImageTk import PhotoImage
from PIL import Image


white = 0
black = 1


"""
All pieces:
	valid_placements method returns a list of tuples containing positions in the 2D array
	display method gets passed the_canvas and draw whatever is stored in self._image
"""


class Pawn:

	def __init__(self, color):
		self.color = color
		image = Image.open(f'piece_images/pawn_{get_piece_color(color)}.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self._image = PhotoImage(image)

	def valid_placements(self, col, row, board):
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

		return placements

	def display(self,x,y, the_canvas):
		the_canvas.create_image(x,y, image=self._image)




class Rook:

	def __init__(self, color):
		self.color = color
		image = Image.open(f'piece_images/rook_{get_piece_color(color)}.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self._image = PhotoImage(image)


	def valid_placements(self, col, row, board):
		placements = []
		for d in [(-1,0),(0,1),(1,0),(0,-1)]:
			ncol,nrow = col + d[0], row + d[1]
			while True:
				if 0 <= nrow <= 7 and 0 <= ncol <= 7:
					spot = board[ncol][nrow]
					placements.append((ncol, nrow))
					ncol,nrow = ncol + d[0], nrow + d[1]
					if spot:
						if spot.color == self.color:
							placements.remove((ncol - d[0],nrow - d[1]))
						break
				else:
					break
		return placements

	def display(self,x,y, the_canvas):
		the_canvas.create_image(x,y, image=self._image)




class Bishop:

	def __init__(self, color):
		self.color = color
		image = Image.open(f'piece_images/bishop_{get_piece_color(color)}.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self._image = PhotoImage(image)


	def valid_placements(self, col, row, board):
		placements = []
		for d in [(-1,-1),(-1,1),(1,1),(1,-1)]:
			ncol,nrow = col + d[0], row + d[1]
			while True:
				if 0 <= nrow <= 7 and 0 <= ncol <= 7:
					spot = board[ncol][nrow]
					placements.append((ncol, nrow))
					ncol,nrow = ncol + d[0], nrow + d[1]
					if spot:
						if spot.color == self.color:
							placements.remove((ncol - d[0],nrow - d[1]))
						break
				else:
					break
		return placements

	def display(self,x,y, the_canvas):
		the_canvas.create_image(x,y, image=self._image)




class Knight:

	def __init__(self, color):
		self.color = color
		image = Image.open(f'piece_images/knight_{get_piece_color(color)}.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self._image = PhotoImage(image)


	def valid_placements(self, col, row, board):
		placements = []
		for d in [(-2,-1),(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2)]:
			ncol,nrow = col + d[0], row + d[1]
			if 0 <= nrow <= 7 and 0 <= ncol <= 7:
				spot = board[ncol][nrow]
				placements.append((ncol, nrow))
				ncol,nrow = ncol + d[0], nrow + d[1]
				if spot:
					if spot.color == self.color:
						placements.remove((ncol - d[0],nrow - d[1]))

		return placements

	def display(self,x,y, the_canvas):
		the_canvas.create_image(x,y, image=self._image)




class Queen(Rook, Bishop):

	def __init__(self, color):
		self.color = color
		image = Image.open(f'piece_images/queen_{get_piece_color(color)}.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self._image = PhotoImage(image)


	def valid_placements(self, col, row, board):
		placements = Rook.valid_placements(self, col, row, board) + Bishop.valid_placements(self, col, row, board)
		return placements

	def display(self,x,y, the_canvas):
		the_canvas.create_image(x,y, image=self._image)




class King(Queen):

	def __init__(self, color):
		self.color = color
		image = Image.open(f'piece_images/king_{get_piece_color(color)}.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self._image = PhotoImage(image)


	def valid_placements(self, col, row, board):
		placements = Queen.valid_placements(self, col, row, board)
		placements = filter(lambda spot: -1 <= spot[0] - col <= 1 and -1 <= spot[1] - row <= 1, placements)
		return placements

	def display(self,x,y, the_canvas):
		the_canvas.create_image(x,y, image=self._image)


def get_piece_color(color):
	"""returns the string white or black instead of the tkinter color name normally stored"""
	if color is white:
		return 'white'
	else:
		return 'black'
