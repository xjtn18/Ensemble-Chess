from tkinter import Tk,Canvas
from chess_view import *

#Globals


class Motion:
	"""tracks the position of the cursor relative to the canvas"""
	def __init__(self):
		self.x = 0
		self.y = 0

	def motion(self, event):
	    self.x, self.y = event.x, event.y

	def get_pos(self):
		return self.x,self.y


if __name__ == '__main__':
	root = Tk()
	root.title("Jake Chess")
	root.protocol("WM_DELETE_WINDOW",quit)
	root.resizable(False, False)

	the_canvas = Canvas(root,width=600,height=600,bg="gray10")
	the_canvas.pack()


	#Bindings
	the_canvas.bind("<ButtonPress>", lambda event : game.gamestate.mouse_click(event.x,event.y))
	my_motion = Motion()
	the_canvas.bind('<Motion>', my_motion.motion)


	game = ChessGame(my_motion)

	def repeater(root):
		game.display(the_canvas)
		root.after(20,repeater,root)

	repeater(root)
	root.mainloop()


