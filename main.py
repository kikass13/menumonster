#deps
import time
import sys
import os
import inspect
import tty
import termios

#pip install texttable
#import texttable as tt

#internal classes
from classes.Monster import Monster



class SomeClass:
	def __init__(self, name, author, id):
		self.name = name
		self.author = author
		self.id = id
		self.useless = "imaUselessBastard"
	def someFunction():
		pass


#############################################################################

content = 	[
				SomeClass("blaaaaaaaaaaa", "nick", "11283Z3"),
				SomeClass("sfdgdfgetztrzhfgh", "samn", "112x23"),
				SomeClass("xaxaaxaxaxaxa", "hulnk", "77761"),
				SomeClass("meh, lappen", "nlop", "66684XZa1"),
			]
#############################################################################


def main(argv):

	#loading bar
	#for i in range(100):
	#	time.sleep(0.01)
	#	sys.stdout.write("\r%d%%" % i)
	#	sys.stdout.flush()
	selectedItem = None

	mainformat = "$(id)$ | $(author)$ | $(name)$ "
	detailformat = "EXTRAlel:$(useless)$ | $(name)$:$(name)$"	#string:key | .... if string is also a key, we use the name of that key as placeholder
	m = Monster("fancy", content, mainFormat=mainformat, detailFormat=detailformat)
	selectedItem = m.interactive()

	print("xaxaaxa: ")
	print("xaxaxa: ")
	if(selectedItem is not None):
		print("i choose an item: ")
		print(selectedItem)
		print("i choose an item: ")
		print("i choose an item: ")
		print("i choose an item: ")
		print("i choose an item: ")
		print("i choose an item: ")
		print("i choose an item: ")



#############################################################################

if __name__ == "__main__":
	main(sys.argv)