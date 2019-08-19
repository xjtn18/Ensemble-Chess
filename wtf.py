"""
This proves that in python, when working with class attributes, storing the list items in a variable and
changing that variable does actually change the items inthe list themselves, and so this gets rid of the need
to constantly reference the items int eh list using indexing.

"""

import math

class Thing:
	def __init__(self):
		self.bro = 5


class Test:
	def __init__(self):
		self.listt = [Thing(), Thing()]

	def update(self):
		#thing = self.listt[0]
		for thing in self.listt:
			self.change(thing)

	def change(self, thing):
		thing.bro = 7

	def show(self):
		for thing in self.listt:
			print(thing.bro, end=" ")
		print("")

	def distance(self, p1, p2):
		x1,y1 = p1
		x2,y2 = p2
		return math.sqrt((y2 - y1)**2 + (x2 - x1)**2)





test = Test()
test.show()
test.update()
test.show()

test_list = ["blue", "red"]


for i in test_list:
	print(i, end=" ")
print(" ")

test.distance((264,492), (264, 340))



