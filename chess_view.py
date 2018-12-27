from chess_model import *
import chess_script


class ChessGame:
	def __init__(self, my_motion):
		self.gamestate = ChessModel()
		self.mouse_pos = my_motion	# Stores the position of the mouse relative to the canvas


	def display(self, the_canvas):
		"""Displays everything on the canvas"""
		for o in the_canvas.find_all():
			the_canvas.delete(o)

		w = the_canvas.winfo_height()
		sh = w/8


		# This block displays the board and pieces (the game is still playing)
		if self.gamestate and not chess_model.WINNER:
			self.draw_board(the_canvas, w, sh)
			self.draw_hints(the_canvas, w, sh)
			self.draw_pieces(the_canvas, w, sh)

		#This block, when first executed, deletes the gamestate; then it repeatedly
			# displays the game over screen
		else:
			if self.gamestate:
				self.gamestate = None
				the_canvas.unbind("<ButtonPress>")
			self.draw_end_game(the_canvas, w, chess_model.WINNER)




	def draw_board(self, the_canvas, w, sh):
		square_color = 'burlywood3'
		for col in range(8):
			square_color = self.swap_color(square_color)
			for row in range(8):
				the_canvas.create_rectangle(col*sh,w-(row*sh),col*sh+sh,w-(row*sh+sh),fill=square_color,outline=square_color)
				square_color = self.swap_color(square_color)


	def draw_hints(self, the_canvas, w, sh):
		"""Draws hint colors that show selected, destinations, and captures"""
		if self.gamestate.selection:
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
								#if type(self.gamestate.board[dcol][drow]) is not King:
								the_canvas.create_rectangle(dcol*sh,w-(drow*sh),dcol*sh+sh,w-(drow*sh+sh),fill='brown3',outline='brown3')
								#else:
									#the_canvas.create_rectangle(dcol*sh,w-(drow*sh),dcol*sh+sh,w-(drow*sh+sh),fill='steelblue3',outline='steelblue3')



	def draw_pieces(self, the_canvas, w, sh):
		for col in range(8):
			for row in range(8):
				piece = self.gamestate.board[col][row]
				if piece:
					# Call display on each piece
					piece.display(col*sh + sh/2 - 1, w - (row*sh + sh/2), the_canvas)



	def swap_color(self, square_color):
		"""For checkerboard pattern"""
		if square_color == 'burlywood3':
				square_color = 'sienna4'
		else:
			square_color = 'burlywood3'
		return square_color


	def draw_end_game(self, the_canvas, w, winner):
		"""Draws the end game screen (shows who won)"""
		if winner is white:
			winner_text = 'white'
			the_canvas.configure(background='gray10')
			text_fill = 'ghost white'
		else:
			winner_text = 'black'
			the_canvas.configure(background='ghost white')
			text_fill = 'gray10'
		text = f"{winner_text}  wins"
		the_canvas.create_text(w/2 - len(text)/2, w/2-15,fill=text_fill,font=('Herculanum', 50),
                    	text=text)

