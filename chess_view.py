from chess_model import *
import chess_script
from PIL.ImageTk import PhotoImage
from PIL import Image


def get_piece_color(color):
	"""returns the string white or black instead of the tkinter color name normally stored"""
	if color is white:
		return 'white'
	else:
		return 'black'


class ChessGame:
	def __init__(self, my_motion):
		self.gamestate = ChessModel()
		self.mouse_pos = my_motion	# Stores the position of the mouse relative to the canvas

		self.white_bishop = Image.open('piece_images/bishop_white.png')
		self.white_king = Image.open('piece_images/king_white.png')
		self.white_queen = Image.open('piece_images/queen_white.png')
		self.white_rook = Image.open('piece_images/rook_white.png')
		self.white_knight = Image.open('piece_images/knight_white.png')
		self.white_pawn = Image.open('piece_images/pawn_white.png')

		self.black_bishop = Image.open('piece_images/bishop_black.png')
		self.black_king = Image.open('piece_images/king_black.png')
		self.black_queen = Image.open('piece_images/queen_black.png')
		self.black_rook = Image.open('piece_images/rook_black.png')
		self.black_knight = Image.open('piece_images/knight_black.png')
		self.black_pawn = Image.open('piece_images/pawn_black.png')

		self.white_bishop = self.white_bishop.resize((75, 75), Image.ANTIALIAS)
		self.white_king = self.white_king.resize((75, 75), Image.ANTIALIAS)
		self.white_queen = self.white_queen.resize((75, 75), Image.ANTIALIAS)
		self.white_rook = self.white_rook.resize((75, 75), Image.ANTIALIAS)
		self.white_knight = self.white_knight.resize((75, 75), Image.ANTIALIAS)
		self.white_pawn = self.white_pawn.resize((75, 75), Image.ANTIALIAS)

		self.black_bishop = self.black_bishop.resize((75, 75), Image.ANTIALIAS)
		self.black_king = self.black_king.resize((75, 75), Image.ANTIALIAS)
		self.black_queen = self.black_queen.resize((75, 75), Image.ANTIALIAS)
		self.black_rook = self.black_rook.resize((75, 75), Image.ANTIALIAS)
		self.black_knight = self.black_knight.resize((75, 75), Image.ANTIALIAS)
		self.black_pawn = self.black_pawn.resize((75, 75), Image.ANTIALIAS)





	def display(self, the_canvas):
		"""Displays everything on the canvas"""
		for o in the_canvas.find_all():
			the_canvas.delete(o)

		w = the_canvas.winfo_height()
		sh = w/8


		# This block displays the board and pieces (the game is still playing)
		if self.gamestate and not self.gamestate.winner:
			self.draw_board(the_canvas, w, sh)
			self.draw_hints(the_canvas, w, sh)
			self.draw_pieces(the_canvas, w, sh)

		#This block, when first executed, deletes the gamestate; then it repeatedly
			# displays the game over screen
		else:
			if self.gamestate:
				self.gamestate = None
				the_canvas.unbind("<ButtonPress>")
			self.draw_end_game(the_canvas, w, self.gamestate.winner)




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
					x = col*sh + sh/2 - 1
					y = w - (row*sh + sh/2)


					if type(piece) is Pawn:
						if piece.color == white:
							the_canvas.create_image(x, y, image=PhotoImage(self.white_pawn))
						else:
							the_canvas.create_image(x, y, image=PhotoImage(self.black_pawn))
						#piece.display(x,y,the_canvas)


					elif type(piece) is Bishop:
						if piece.color == white:
							the_canvas.create_image(x, y, image=PhotoImage(self.white_bishop))
						else:
							the_canvas.create_image(x, y, image=PhotoImage(self.black_bishop))


					elif type(piece) is Rook:
						if piece.color == white:
							the_canvas.create_image(x, y, image=PhotoImage(self.white_rook))
						else:
							the_canvas.create_image(x, y, image=PhotoImage(self.black_rook))


					elif type(piece) is Knight:
						if piece.color == white:
							the_canvas.create_image(x, y, image=PhotoImage(self.white_knight))
						else:
							the_canvas.create_image(x, y, image=PhotoImage(self.black_knight))


					elif type(piece) is Queen:
						if piece.color == white:
							the_canvas.create_image(x, y, image=PhotoImage(self.white_queen))
						else:
							the_canvas.create_image(x, y, image=PhotoImage(self.black_queen))


					else: # King
						if piece.color == white:
							the_canvas.create_image(x, y, image=PhotoImage(self.white_king))
						else:
							the_canvas.create_image(x, y, image=PhotoImage(self.black_king))




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


