from tkinter import Tk,Canvas, Toplevel
from chess_view import *
from chess_sound import *

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


def center(root):
	root.withdraw()
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	window_width = root.winfo_width()
	window_height = root.winfo_height()
	x = screen_width/2 - window_width/2
	y = screen_height/2 - window_height/2
	root.geometry('%dx%d+%d+%d' %  (window_width,window_height, x, y))
	root.deiconify()



if __name__ == '__main__':
	root = Tk()

	root.title("Ensemble Chess")
	root.protocol("WM_DELETE_WINDOW",quit)

	the_canvas = Canvas(root,width=600,height=600,bg="gray10")
	the_canvas.pack()
	root.update_idletasks()

	center(root)
	
	root.resizable(False, False)

	#Bindings
	the_canvas.bind("<ButtonPress>", lambda event : game.gamestate.mouse_click(event.x,event.y))
	my_motion = Motion()
	the_canvas.bind('<Motion>', my_motion.motion)

	game = ChessGame(my_motion, root)

	# Main loop
	def repeater(root):
		game.display(the_canvas)
		root.after(1,repeater,root)

	repeater(root)
	root.mainloop()




