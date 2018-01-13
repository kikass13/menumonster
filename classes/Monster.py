#deps
import os
import sys

#pip install texttable
import texttable as tt

import curses

from MonsterItem import MonsterItem
from Color import Color

#from termcolor import colored
#print(colored('hello', 'red'))


######################################################################################
class Monster:
	# class variable shared by all instances
	leftValDelim = "$("
	rightValDelim = ")$"

	#kind = 'canine'
	def __init__(self, type, content, format):
		self.type = type    # instance variable unique to each instance
		self.format = format
		self.items = []
		self.align = "center"
		#do something usefull
		self.interpretKeys()
		for i, obj in enumerate(content):
			self.items.append(MonsterItem(i, obj, self.header, format))
		#define first selected item :)
		self.selectedItem = self.items[0]
		self.skipLines = 3 #amount for useless lines (top )



	def init(self):
		pass


	def interpretKeys(self):
		formatKeys = []
		#seperate formats
		replacers = self.format.split("|")
		#find keys in formatstrings
		for r in replacers:
			delim = r[r.find(self.leftValDelim) + len(self.leftValDelim):r.find(self.rightValDelim)]
			if(delim is not ""):
				formatKeys.append(delim)
		self.header = formatKeys


	def clear(self):
		os.system('clear')  # on linux / os 

	def alignTable(self, table):
		#grab tty size (in characters), see https://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python
		rows, columns = os.popen('stty size', 'r').read().split()
		#how long is this table?
		length = 0
		for line in table:
			if len(line) > length:
				length = len(line)
		if(self.align == "center"):
			#try to centroid it
			div = (float(columns) / float(length) / 2)
			#print(int(div * length))
			spaces = " " * int(div * length - length/2)
		#add spaces
		for i, line in enumerate(table):
			line = spaces + line 
			table[i] = line
		return table

	def generateTable(self):
		#see https://github.com/foutaise/texttable
		tab = tt.Texttable()
		#grb header keys
		tableHeader = ["#"]
		#append an arbitrary number on front
		for key in self.header:
			tableHeader.append(key)
		####################################
		align=[]
		for key in tableHeader: align.append("l")		# "l", "r", "c"
		tab.set_cols_align(align)
		valign=[]
		for key in tableHeader: valign.append("m")
		tab.set_cols_valign(valign)
		tab.set_deco(tab.HEADER | tab.BORDER | tab.VLINES) 	## no tab.HLINES
		#set the header to the table
		tab.header(tableHeader)
		####################################
		####################################
		#prepare contents
		matrix = []
		for item in self.items:
			row = []
			#dont forget the arbitrary number on front ! :)
			row.append(item.id)
			for i, key in enumerate(self.header):
				row.append(item.get(key))
			matrix.append(row)
		for row in matrix:
			tab.add_row(row)
		####################################
		#grab table
		tablestr = tab.draw()
		tablestrs = tablestr.split("\n")
		return tablestrs


	def render(self, color=True):
			self.clear()
			table = self.generateTable()
			if(color):
				table = self.colorizeTable(table)
			table = self.alignTable(table)
			table = self.serializeTable(table)
			return table

	def show(self):
		table = self.render()
		self.printTable(table)



	def colorizeTable(self, table):
		#split into lines printed
		for i, line in enumerate(table):
			if self.selectedItem.id == i - self.skipLines:
				line = self.colorLine(line, "WHITE", "RED", False)
			else:
				line = self.colorLine(line, "WHITE", "Black", False)
			table[i] = line
		return table



	def colorLine(self, line, fg="WHITE", bg="BLACK", bold=False):
		line = self.colorText(line, fg, bg , bold)
		return line

	#see https://stackoverflow.com/questions/2330245/python-change-text-color-in-shell
	#http://ascii-table.com/ansi-escape-sequences.php
	def colorText(self, string, fg="WHITE", bg="BLACK", bold=False):
		bold = "0"
		if bold:
			bold = "1"
		fg = Color.getFg(fg)
		bg = Color.getBg(bg)
		attrStr = bold + ";" + fg + ";" + bg + "m" + string
		#print(attrStr + "\n")
		return ("\x1b[%s\x1b[0m" % attrStr)		#type(bold etc) ; forground color ; background color 'm' String


	def serializeTable(self, table):
		string = ""
		for i, line in enumerate(table):
			string += line + "\r\n"
		return string

	def printTable(self, table):
		print(table)



	def up(self):
		newIndex = self.selectedItem.id
		if newIndex > 0:
			newIndex = newIndex - 1
		self.selectedItem = self.items[newIndex]

	def down(self):
		newIndex = self.selectedItem.id
		if newIndex < len(self.items) - 1:
			newIndex = newIndex + 1
		self.selectedItem = self.items[newIndex]




#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################


		#inputloop for arrow keys
	def input(self):

		# get the curses screen window
		screen = curses.initscr()
		self.screen = screen
		#Must be called if the programmer wants to use colors, and before any other color manipulation routine is called. It is good practice to call this routine right after initscr().
		curses.start_color()
		curses.use_default_colors()	#0 to 7
		# turn off input echoing
		curses.noecho()
		# respond to keys immediately (don't wait for enter)
		curses.cbreak()
		# map arrow keys to special values
		screen.keypad(True)

		#table = self.show()

		#this will whow the display screen even when no button is pressed
		#screen.getch() will do a clearscreen ... so we dont have an output if we dont use this line! :??
		curses.halfdelay(1)           # How many tenths of a second are waited, from 1 to 255

		once=True
###############################################################
		try:
			while True:
				char = screen.getch()
				if(once):
					curses.halfdelay(255)
					once = False
				if char == ord('q'):
					break
				elif char == 27:
					# Don't wait for another key
					# If it was Alt then curses has already sent the other key
					# otherwise -1 is sent (Escape)
					#self.screen.nodelay(True)
					#n = self.screen.getch()
					#if n == -1:
					# Escape was pressed
					break
				else:

					#and check function of keys
					if char == curses.KEY_RIGHT:
						pass #screen.addstr(30, 0, 'right') # print doesn't work with curses, use addstr instead
					elif char == curses.KEY_LEFT:
						pass	#screen.addstr(30, 0, 'left ')    
					elif char == curses.KEY_UP:
						self.up() #screen.addstr(30, 0, 'up   ') 
						
					elif char == curses.KEY_DOWN:
						self.down() #screen.addstr(30, 0, 'down ')
					elif char == curses.KEY_ENTER:
						screen.addstr(30, 0, 'ENTER ')
						
					#else:
						#other .. print it
					#	screen.addstr(30, 30, str()) 


					#normal key was pressed, react
					#reprint table
					table = self.show()

					
					
		finally:
			# shut down cleanly
			curses.nocbreak(); screen.keypad(0); curses.echo()
			curses.endwin()

			
