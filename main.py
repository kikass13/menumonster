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
				SomeClass("blaaaaaaaaaaa", "nick", "112833"),
				SomeClass("sfdgdfgetztrzhfgh", "sam", "11223"),
				SomeClass("xaxaaxaxaxaxa", "hulk", "7776"),
				SomeClass("meh, lappen", "nlop", "66684Xa"),
			]
#############################################################################


def main(argv):

	#for i, obj in enumerate(content):
	#	for attribute, value in obj:
	#		print("%s : %s" % (attribute, value))
	#loading bar
	#for i in range(100):
	#	time.sleep(0.01)
	#	sys.stdout.write("\r%d%%" % i)
	#	sys.stdout.flush()

	m = Monster("fancy", content, "$(id)$ | $(author)$ | $(name)$")
	#m.show()
	#for line in m.render(color=True, serialize=False):
	#	sys.stdout.write(line)
	m.display()


#############################################################################

if __name__ == "__main__":
	main(sys.argv)