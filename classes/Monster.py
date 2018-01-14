#deps
import os
import sys
import time 

#pip install texttable
import texttable as tt

import curses
from curses import panel   

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
		self.position = 0
		self.skipLines = 3 #amount for useless lines (top )
		self.tableHeight = 0
		self.tableLeft = 0

		self.extendedItems = [] 

		#screen thingys thanks to curse
		stdscreen = curses.initscr()
		curses.start_color()
		curses.use_default_colors()
		self.window = stdscreen.subwin(0,0)
		self.window.keypad(1)
		self.panel = panel.new_panel(self.window)
		self.panel.hide()
		panel.update_panels()



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
		spaces = ""
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
		self.tableLeft = len(spaces)
		return table


	def extendItems(self, table):
		newTable = []
		for index, line in enumerate(table):
			newTable.append(line)
			if(index < self.skipLines):
				continue
			for item in self.items:
				if(index - self.skipLines == item.id):
					if(item.isExpanded()):
						#probably add left table seperator ?! "|"
						newTable.append("|\t -- " + item.details())
		return newTable


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
		#print(repr(tablestr))
		#tablestr = tablestr.replace("\n", "\r\n.!?")
		tablestrs = tablestr.split("\n")
		self.tableHeight = len(tablestrs)
		#print(tablestrs)
		#print("BLABLA: %s" % len(tablestrs))
		#for line in tablestrs:
		#	print(repr(line)+"\r")
		#print("\n\n\n\n\n\n")
		#but please dont delete the "\n"
		#print(tablestrs)
		return tablestrs


	def render(self, color=True, serialize=False):
			table = self.generateTable()
			if(color):
				table = self.colorizeTable(table)
			#testi extension
			table = self.extendItems(table)
			###
			table = self.alignTable(table)
			if(serialize):
				table = self.serializeTable(table)
			return table


	def show(self):
		#self.clear()
		serializedTable = self.render(color=True, serialize=True)
		self.printTable(serializedTable)


	def printLine(self, line):
		sys.stdout.write(line+"\r\n")


	def printTable(self, serializedTable):
		for index, line in enumerate(self.render(color=True, serialize=False)):
			self.printLine(line)


	def colorizeTable(self, table):
		#split into lines printed
		for i, line in enumerate(table):
			if self.position + self.skipLines == i:
				line = self.colorLine(line, "WHITE", "RED", False)
			else:
				line = self.colorLine(line, "WHITE", "BLACK", False)
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
			string += line
		return string


	def navigate(self, n):
		self.position += n
		if self.position < 0:
			self.position = 0
		elif self.position >= len(self.items):
			self.position = len(self.items)-1


#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################


	def display(self):
		self.panel.top()
		self.panel.show()
		self.window.clear()

		#random variabls heping in displax
		self.unknownBuffer = ""
		self.inputBuffer = ""
		test = "|"
		#curses.init_color(1337, 0, 0, 0)	## not working
		curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

		#main display loop
		while True:

			#pre refresh
			maxheight, maxwidth = self.window.getmaxyx()
			#refresh
			self.window.clear()	#this is usefull, because if something is drawn like
			# "123ab" and we draw "xy" at the same position 
			# the result on the screen will be "xy3ab", because the rest wasnt properly cleared

			self.window.refresh()	#redraws the screen buffer
			curses.doupdate()
			#post refresh
			##  drawing 
			########################
			if(test == "|"): test = "/"
			elif test == "/": test = "~"
			elif test == "~": test = "\\"
			elif test == "\\": test = "|"

			self.window.addstr(maxheight-1,0, test)

			#self.show()
			table = self.render()
			self.printTable(table)
			#need to implement a menu api for generating a menu based on a filter of self.items
			#input characters will define search strings for all keys inside of self.items
			#need to implement submenu functionality
			#pressing + key should list extra information in our table  below the current selected entry 


			#16.02. broesel bday ;)


			self.window.addstr(self.tableHeight + 2 , self.tableLeft, "===> " + self.inputBuffer, curses.A_NORMAL)
			self.window.addstr(maxheight-1,maxwidth-15, "-> " + self.unknownBuffer, curses.A_NORMAL)

			########################
			key = self.window.getch()
			action = self.input(key)
			if(action == "exit"):
				break

			#if we draw (double) after getch, we can "overwrite" specific things if text is not properly drawn
			#self.window.addstr(maxheight-1,maxwidth-15, "-> " + "      ", curses.A_NORMAL)

		self.window.clear()
		self.panel.hide()
		panel.update_panels()
		curses.doupdate()


	#inputloop for arrow keys
	def input(self, key):
		ret = "ok"

		if key == ord('q'):
			ret = "exit"
		elif key == 27:
			# Don't wait for another key
			# If it was Alt then curses has already sent the other key
			# otherwise -1 is sent (Escape)
			#self.screen.nodelay(True)
			#n = self.screen.getch()
			#if n == -1:
			# Escape was pressed
			ret = "exit"
		###########
		else:
			#and check arrow of keys
			if key == curses.KEY_RIGHT:
				pass #screen.addstr(30, 0, 'right') # print doesn't work with curses, use addstr instead
			elif key == curses.KEY_LEFT:
				pass	#screen.addstr(30, 0, 'left ')    
			elif key == curses.KEY_UP:
				self.navigate(-1)
			elif key == curses.KEY_DOWN:
				self.navigate(1)

			#if key in [curses.KEY_ENTER, ord('\n')]:
			elif key in [curses.KEY_ENTER, ord('\n')]:
				self.selectedItem = self.items[self.position]
			###############################################
			#command keys
			elif key == 9:	# 9 = TAB	# ++++ = 49 #
				item = self.items[self.position]
				#check if not allready extended
				if(item.isExpanded()):
					item.contract()
				else:
					item.expand()

			elif key == curses.KEY_BACKSPACE: #263
				self.inputBuffer = self.inputBuffer[:len(self.inputBuffer)-1]
			###############################################
			#character input
			elif key >= 32 and key <= 126:
				self.inputBuffer += str(unichr(key))
			#unknown input
			else:
				pass
				#negative values are KEYUP events???
				#ignore them for now plx
				if(key > 0 ):
					self.unknownBuffer = str(key)
				else:
					pass
		return ret
