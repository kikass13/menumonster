#deps
import os
import sys
import time 

#pip install texttable
import texttable as tt

import curses
from curses import panel   

from MonsterItem import MonsterItem
from MonsterTable import MonsterTable
from Color import Color


######################################################################################
class Monster:

	#kind = 'canine'
	def __init__(self, type, content, mainFormat="", detailFormat="", exitString="", exitType="INVISIBLE", align="center"):
		self.type = type    # instance variable unique to each instance
		
		self.mainFormat = mainFormat
		self.detailFormat = detailFormat
		self.align = align
		self.exitType = exitType			#exitType = "NONE" will disable menu Exit with 'q' or 'esc'

		self.items = []
		for i, obj in enumerate(content):
			self.items.append(MonsterItem(i, obj))
		
		#define first selected item :)
		self.position = 0

		self.expandedItems = [] 
		self.localItemList = self.items
		self.localFilteredItemList = []

		#screen thingys thanks to curse
		print("1")
		self.stdscreen = curses.initscr()
		curses.start_color()
		curses.use_default_colors()
		self.window = self.stdscreen.subwin(0,0)
		self.window.keypad(1)
		print(self.window)
		self.panel = panel.new_panel(self.window)
		self.panel.hide()
		panel.update_panels()

		self.table = MonsterTable(self, self.mainFormat, self.detailFormat)

		self.selectedItem = None

#############################################################################################################################################################################################
#############################################################################################################################################################################################
#############################################################################################################################################################################################

	#wrapper for exceptions, tty cleanup (curses mess) and return value definition
	def interactive(self):
		ret = None
		try:
			ret = self.display()
		except KeyboardInterrupt as e:
			curses.endwin()
			print("KeyboardInterrupt")
			pass
		#except Exception as e:
		#	raise e
		
		#clean up the mess curses did
		os.system('stty sane;clear')
		return ret

		
	def display(self):
		self.panel.top()
		self.panel.show()
		print(self.window)
		self.window.clear()

		#random variabls heping in displax
		self.unknownBuffer = ""
		self.inputBuffer = ""
		test = "|"
		#curses.init_color(1337, 0, 0, 0)	## not working
		curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

		#allow setting of cursor (via setxy)
		curses.curs_set(1)

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


			#skip some y lines  (trim on top)
			topLines = 1
			curses.setsyx(topLines,0)
			curses.doupdate()

			#draw table with current information
			self.table.show(position = self.position, items = self.localItemList)

			#need to implement a menu api for generating a menu based on a filter of self.items
			#input characters will define search strings for all keys inside of self.items
			#need to implement submenu functionality

			#16.02. broesel bday ;)

			exitmsg ="Press 'q' For Exit"
			#self.window.addstr(self.table.tableHeight + topLines + 1 , self.table.tableLeft, "Select item:\t\t" + exitmsg, curses.A_NORMAL)
			self.window.addstr(maxheight-1,maxwidth-15, "-> " + self.unknownBuffer, curses.A_NORMAL)
			self.window.addstr(maxheight-1, 3, "Select item...", curses.A_NORMAL)

			#perfect center for this msg
			off = (self.table.tableLeft + self.table.tableWidth/2) - int(len(exitmsg))
			self.window.addstr(maxheight-1, off, exitmsg, curses.A_NORMAL)

			self.window.addstr(self.table.tableHeight + topLines + 2 , self.table.tableLeft, "===> " + self.inputBuffer, curses.A_NORMAL)
			########################

			key = self.window.getch()

			action = self.input(key)
			if(action == "exit"):
				break

		#clean up the curses mess :)
		self.window.clear()
		self.panel.hide()
		panel.update_panels()
		curses.doupdate()
		#delete the window, and do some shit so that we "turn back" to our normal shell
		curses.endwin()
		del self.window
		del self.stdscreen

		#return all information about the selected item to calling instance##
		if(self.selectedItem is not None):
			return self.selectedItem.data
		

		

	def filterItems(self):
		itemList = []
		filteredItems = []
		for item in self.items:
			if(self.inputBuffer == "" or item.search(self.inputBuffer) == True):
				itemList.append(item)
			else:
				filteredItems.append(item)
		self.localItemList = itemList
		self.localFilteredItemList = filteredItems
		#renavigate to update position
		self.navigate(0)


	def navigate(self, n):
	#	self.position += n
	#	elif self.position < 0 :
	#		self.position = 0
	#	elif self.position >= len(self.localItemList):
	#		self.position = len(self.localItemList)-1
		if len(self.localItemList) == 0:
			self.position = -1
		else:
			self.position += n
			if self.position <= 0:
				self.position = 0
			elif self.position >= len(self.localItemList):
				self.position = len(self.localItemList)-1



	#inputloop for arrow keys
	def input(self, key):
		ret = "ok"

		if key == ord('q') or key == 27:
			if(self.exitType is not "NONE"):
				ret = "exit"
			# Don't wait for another key
			# If it was Alt then curses has already sent the other key
			# otherwise -1 is sent (Escape)
			#self.screen.nodelay(True)
			#n = self.screen.getch()
			#if n == -1:
			# Escape was pressed
		#	ret = "exit"
		###########
		#else:
		#and check arrow of keys
		elif key == curses.KEY_RIGHT:
			pass #screen.addstr(30, 0, 'right') # print doesn't work with curses, use addstr instead
		elif key == curses.KEY_LEFT:
			pass	#screen.addstr(30, 0, 'left ')    
		elif key == curses.KEY_UP:
			self.navigate(-1)
		elif key == curses.KEY_DOWN:
			self.navigate(1)

		#if key in [curses.KEY_ENTER, ord('\n')]:
		elif key in [curses.KEY_ENTER, ord('\n')]:
			#if inputbuffer does not contain a digit(number)
			#that way we can still enter a number for our chosen thing
			if(len(self.inputBuffer) < 3 and self.inputBuffer.isdigit()):
				try:
					self.selectedItem = self.localItemList[int(self.inputBuffer)]
					ret = "exit"
				except Exception as e:
					pass
			else:
				try:
					self.selectedItem = self.localItemList[self.position] #choose the selected item
					ret = "exit"
				except Exception as e:
					pass
		###############################################
		#command keys
		elif key == 9:	# 9 = TAB	# ++++ = 49 #
			if(self.position is not -1):
				item = self.localItemList[self.position]
				#check if not allready extended
				if(item.isExpanded()):
					item.contract()
				else:
					item.expand()

		elif key == curses.KEY_BACKSPACE: #263
			self.inputBuffer = self.inputBuffer[:len(self.inputBuffer)-1]
			self.filterItems()

		###############################################
		#character input
		elif key > 32 and key <= 126:			#32 is space, dont use this in filter
			self.inputBuffer += str(unichr(key))
			#only apply filter if more than 1 character was inputted
			#this only works if the inputted string is not a NUMBER
			if(len(self.inputBuffer) > 2 or self.inputBuffer.isdigit() == False ):
				self.filterItems()

		#print input
		#negative values are KEYUP events???
		#ignore them for now plx
		if(key > 0 ):
			self.unknownBuffer = str(key)
			

		return ret
