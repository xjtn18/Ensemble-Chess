from chess_model import *
import chess_script
from PIL.ImageTk import PhotoImage
from PIL import Image


def get_piece_color(color):
	"""returns the string white or black instead of the tkinter color name normally stored"""
	return 'white' if color is white else 'black'



class ChessGame:
	def __init__(self, my_motion, root):
		self.root = root
		self.gamestate = ChessModel(root)
		self.mouse_pos = my_motion	# Stores the position of the mouse relative to the canvas


		image = Image.open('piece_images/bishop_white.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self.white_bishop = PhotoImage(image)

		image = Image.open('piece_images/rook_white.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self.white_rook = PhotoImage(image)

		image = Image.open('piece_images/knight_white.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self.white_knight = PhotoImage(image)

		image = Image.open('piece_images/pawn_white.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self.white_pawn = PhotoImage(image)

		image = Image.open('piece_images/queen_white.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self.white_queen = PhotoImage(image)

		image = Image.open('piece_images/king_white.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self.white_king = PhotoImage(image)


		image = Image.open('piece_images/bishop_black.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self.black_bishop = PhotoImage(image)

		image = Image.open('piece_images/rook_black.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self.black_rook = PhotoImage(image)

		image = Image.open('piece_images/knight_black.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self.black_knight = PhotoImage(image)

		image = Image.open('piece_images/pawn_black.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self.black_pawn = PhotoImage(image)

		image = Image.open('piece_images/queen_black.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self.black_queen = PhotoImage(image)

		image = Image.open('piece_images/king_black.png')
		image = image.resize((75, 75), Image.ANTIALIAS)
		self.black_king = PhotoImage(image)


	def update():
		self.root.after(20, chess_script.repeater, self.root)



	def display(self, the_canvas):
		"""Displays everything on the canvas"""
		for o in the_canvas.find_all():
			the_canvas.delete(o)

		w = the_canvas.winfo_height()
		sh = w/8

		ChessModel.w = w
		ChessModel.sh = sh


		# This block displays the board and pieces (the game is still playing)
		if self.gamestate and ChessModel.WINNER == None:
			self.draw_board(the_canvas, w, sh)
			self.draw_hints(the_canvas, w, sh)
			self.draw_pieces(the_canvas, w, sh)

		#This block, when first executed, deletes the gamestate; then it repeatedly
			# displays the game over screen
		else:
			if self.gamestate:
				self.gamestate = None
				the_canvas.unbind("<ButtonPress>")
			self.draw_end_game(the_canvas, w, ChessModel.WINNER)




	def draw_board(self, the_canvas, w, sh):
		square_color = 'SteelBlue2'
		for col in range(8):
			square_color = self.swap_color(square_color)
			for row in range(8):
				the_canvas.create_rectangle(col*sh,w-(row*sh),col*sh+sh,w-(row*sh+sh),fill=square_color,outline=square_color)
				square_color = self.swap_color(square_color)



	def draw_hints(self, the_canvas, w, sh):
		"""Draws hint colors that show selected, destinations, and captures"""
		if self.gamestate.selection:
			col, row = self.gamestate.selection
			the_canvas.create_rectangle(col*sh,w-(row*sh),col*sh+sh,w-(row*sh+sh),fill='DarkOliveGreen3',outline='DarkOliveGreen3')
			for dcol,drow in self.gamestate.selection_placements:
				if self.gamestate.board[dcol][drow] == None:
					mouse_x,mouse_y = self.mouse_pos.get_pos()
					if dcol*sh < mouse_x < dcol*sh + sh and \
						drow*sh < w-mouse_y < drow*sh + sh:
						the_canvas.create_oval(dcol*sh + sh/2.8,w-(drow*sh + sh/2.8),dcol*sh+sh - sh/2.8,w-(drow*sh+sh - sh/2.8),fill='DarkOliveGreen3',outline='DarkOliveGreen3')
					else:
						the_canvas.create_oval(dcol*sh + sh/2.5,w-(drow*sh + sh/2.5),dcol*sh+sh - sh/2.5,w-(drow*sh+sh - sh/2.5),fill='DarkOliveGreen3',outline='DarkOliveGreen3')
				else:
					the_canvas.create_rectangle(dcol*sh,w-(drow*sh),dcol*sh+sh,w-(drow*sh+sh),fill='brown2',outline='brown2')




	def draw_pieces(self, the_canvas, w, sh):
		for col in range(8):
			for row in range(8):
				piece = self.gamestate.board[col][row]
				if piece:
					x = col*sh + sh/2 - 1
					y = w - (row*sh + sh/2)

					if type(piece) is Pawn:
						img = self.white_pawn if piece.color is white else self.black_pawn
					elif type(piece) is Bishop:
						img = self.white_bishop if piece.color is white else self.black_bishop
					elif type(piece) is Rook:
						img = self.white_rook if piece.color is white else self.black_rook
					elif type(piece) is Knight:
						img = self.white_knight if piece.color is white else self.black_knight
					elif type(piece) is Queen:
						img = self.white_queen if piece.color is white else self.black_queen
					else: # King
						img = self.white_king if piece.color is white else self.black_king

					#if piece.location != (x,y):
					#	x, y = piece.location
					x, y = piece.location
					the_canvas.create_image(x, y, image=img)




	def swap_color(self, square_color):
		"""For checkerboard pattern"""
		if square_color == 'SteelBlue2':
			square_color = 'lavender'
		else:
			square_color = 'SteelBlue2'
		return square_color



	def draw_end_game(self, the_canvas, w, winner):
		"""Draws the end game screen (shows who won)"""
		if winner is white:
			winner_text = 'white'
			the_canvas.configure(background='SteelBlue2')
			text_color = 'ghost white'
		else:
			winner_text = 'black'
			the_canvas.configure(background='ghost white')
			text_color = 'SteelBlue2'
		text = f"{winner_text}  wins"
		the_canvas.create_text(w/2 - len(text)/2, w/2-15,fill=text_color,font=('Herculanum', 50),
                    	text=text)


