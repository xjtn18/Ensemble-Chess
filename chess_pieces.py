
# Global
white = 'ghost white'
black = 'gray15'


class Pawn:

	def __init__(self, color):
		self.color = color

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



class Rook:

	def __init__(self, color):
		self.color = color

	def valid_placements(self, col, row, board):
		placements = []
		for d in [(-1,0),(0,1),(1,0),(0,-1)]:
			ncol,nrow = col + d[0], row + d[1]
			while True:
				if 0 <= nrow <= 7 and 0 <= ncol <= 7:
					spot = board[ncol][nrow]
					placements.append((ncol, nrow))
					ncol,nrow = ncol + d[0], nrow + d[1]
					if spot != None:
						if spot.color == self.color:
							placements.remove((ncol - d[0],nrow - d[1]))
						break
				else:
					break
		return placements



class Bishop:

	def __init__(self, color):
		self.color = color

	def valid_placements(self, col, row, board):
		placements = []
		for d in [(-1,-1),(-1,1),(1,1),(1,-1)]:
			ncol,nrow = col + d[0], row + d[1]
			while True:
				if 0 <= nrow <= 7 and 0 <= ncol <= 7:
					spot = board[ncol][nrow]
					placements.append((ncol, nrow))
					ncol,nrow = ncol + d[0], nrow + d[1]
					if spot != None:
						if spot.color == self.color:
							placements.remove((ncol - d[0],nrow - d[1]))
						break
				else:
					break
		return placements



class Knight:

	def __init__(self, color):
		self.color = color

	def valid_placements(self, col, row, board):
		placements = []
		for d in [(-2,-1),(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2)]:
			ncol,nrow = col + d[0], row + d[1]
			if 0 <= nrow <= 7 and 0 <= ncol <= 7:
				spot = board[ncol][nrow]
				placements.append((ncol, nrow))
				ncol,nrow = ncol + d[0], nrow + d[1]
				if spot != None:
					if spot.color == self.color:
						placements.remove((ncol - d[0],nrow - d[1]))

		return placements



class Queen(Rook, Bishop):

	def __init__(self, color):
		self.color = color

	def valid_placements(self, col, row, board):
		placements = Rook.valid_placements(self, col, row, board) + Bishop.valid_placements(self, col, row, board)
		return placements



class King(Queen):

	def __init__(self, color):
		self.color = color

	def valid_placements(self, col, row, board):
		placements = Queen.valid_placements(self, col, row, board)
		placements = filter(lambda spot: -1 <= spot[0] - col <= 1 and -1 <= spot[1] - row <= 1, placements)
		return placements


