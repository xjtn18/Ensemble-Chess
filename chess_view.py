from chess_model import *
import chess_script


class ChessGame:
	def __init__(self, my_motion):
		self.gamestate = ChessModel()
		self.mouse_pos = my_motion

	def display(self, the_canvas):
		for o in the_canvas.find_all():
			the_canvas.delete(o)

		w = the_canvas.winfo_height()
		sh = w/8

		if self.gamestate.winner is None:
			self.draw_board(the_canvas, w, sh)
			self.draw_hints(the_canvas, w, sh)
			self.draw_pieces(the_canvas, w, sh)

		else:
			pass





	def draw_board(self, the_canvas, w, sh):
		square_color = 'burlywood3'
		for col in range(8):
			square_color = self.swap_color(square_color)
			for row in range(8):
				the_canvas.create_rectangle(col*sh,w-(row*sh),col*sh+sh,w-(row*sh+sh),fill=square_color,outline=square_color)
				square_color = self.swap_color(square_color)


	def draw_hints(self, the_canvas, w, sh):
		"""Draws hint colors that show selected, destinations, and captures"""
		if self.gamestate.selection != None:
			for col in range(8):
				for row in range(8):
					if (col, row) == self.gamestate.selection:
						the_canvas.create_rectangle(col*sh,w-(row*sh),col*sh+sh,w-(row*sh+sh),fill='OliveDrab4',outline='OliveDrab4')
						for dcol,drow in self.gamestate.board[col][row].valid_placements(col,row, self.gamestate.board):
							if self.gamestate.board[dcol][drow] == None:
								mouse_x,mouse_y = self.mouse_pos.get_pos()
								if dcol*sh < mouse_x < dcol*sh + sh and \
									drow*sh < w-mouse_y < drow*sh + sh:
									the_canvas.create_oval(dcol*sh + sh/2.8,w-(drow*sh + sh/2.8),dcol*sh+sh - sh/2.8,w-(drow*sh+sh - sh/2.8),fill='OliveDrab4',outline='OliveDrab4')
								else:
									the_canvas.create_oval(dcol*sh + sh/2.5,w-(drow*sh + sh/2.5),dcol*sh+sh - sh/2.5,w-(drow*sh+sh - sh/2.5),fill='OliveDrab4',outline='OliveDrab4')
							else:
								the_canvas.create_rectangle(dcol*sh,w-(drow*sh),dcol*sh+sh,w-(drow*sh+sh),fill='brown3',outline='brown3')


	def draw_pieces(self, the_canvas, w, sh):
		for col in range(8):
			for row in range(8):
				piece = self.gamestate.board[col][row]
				if piece != None:
					the_canvas.create_oval(col*sh + sh/5,w - (row*sh + sh/5),col*sh+sh - sh/5,w - (row*sh+sh - sh/5),fill=piece.color,outline=piece.color)



	def swap_color(self, square_color):
		"""For checkerboard pattern"""
		if square_color == 'burlywood3':
				square_color = 'sienna4'
		else:
			square_color = 'burlywood3'
		return square_color


