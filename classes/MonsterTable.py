#deps
import os
import sys
import time 

#pip install texttable
import texttable as tt

from MonsterItem import MonsterItem
from Color import Color



######################################################################################
class MonsterTable:

	# class variable shared by all instances
	leftValDelim = "$("
	rightValDelim = ")$"

	def __init__(self, parent, mainFormat, detailFormat, color=True):
		self.parent = parent
		#table global information
		self.mainFormat = mainFormat
		self.detailFormat = detailFormat
		self.color = color
		#table attrbibutes
		self.skipLines = 3 # amount for useless lines (top )
		self.tableHeight = 0
		self.tableLeft = 0
		self.align = "center"
		#important attributes from parent
		self.items = None
		self.position = 0
		#table string output buffer)
		self.table = []
		

	def generate(self):
		#see https://github.com/foutaise/texttable
		tab = tt.Texttable()
		#grb header keys
		tableHeader = ["#"]
		#append an arbitrary number on front
		headers = self.interpretMainFormatKeys()
		for key in headers:
			tableHeader.append(key)
		####################################
		align=[]
		for key in tableHeader: align.append("l")		# "l", "r", "c"
		tab.set_cols_align(align)
		valign=[]
		for key in tableHeader: valign.append("t")		# "t", "m", "b"
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
			for i, key in enumerate(headers):
				row.append(item.get(key))
			matrix.append(row)
		for row in matrix:
			tab.add_row(row)
		####################################
		#grab table
		tablestr = tab.draw()
		#print(repr(tablestr))
		#tablestr = tablestr.replace("\n", "\r\n.!?")
		self.table = tablestr.split("\n")
		####################################
		#create Markings of this table for the first time 
		self.recalculateMarkings()
		# ...


	def recalculateMarkings(self):
		#mark all table entrys with their specific line index
		#so that we have a clue how large these entrys are (how many lines)
		#also we have to find the last line (... best guess)
		markings = []
		pos = 0
		count = 0
		proableLastLine = 0
		for i, line in enumerate(self.table):
			#find table number id of this entry
			colstrs = line.split("|")
			try:
				if(colstrs[1].find(str(pos)) > 0):
					markings.append([pos, i])
					pos += 1
			except Exception as e:
				proableLastLine = i
		#after marking the lines, which loooks like this:
		#[[0, 4], [1, 7], [2, 9], [3, 11]]
		#we want to specify the exact entry line count for every entry
		#we want it to look like this:
		#  [entryid , lineIndexInTable, AmountOfLines]
		#[[0, 4, 3], [1, 7, 2], [2, 9, 2], [3, 11, 2]]
		self.tableMarkings = []
		for i, entry in enumerate(markings):
			entryId = entry[0]
			entryLineNumber = entry[1]
			#diff to next entry calc ...
			linecount = -1
			if(i < len(markings)-1):
				linecount = markings[i+1][1] - entryLineNumber
			else:
				linecount = proableLastLine - entryLineNumber
			##add linecount to entry table
			self.tableMarkings.append([entryId, markings[i][1], linecount])
		#print(self.tableMarkings)
		#...


	def printLine(self, line):
		sys.stdout.write(line+"\r\n")

	def show(self, position=0, items = []):
		#set important global information from parent!
		self.items = items
		self.position = position

		#render and draw table 
		self.render()
		for index, line in enumerate(self.table):
			self.printLine(line)


	def render(self, color=True):
		self.generate()
		if(self.color):
			self.colorize()
		self.expandItems()
		self.alignment()


	def expandItems(self):
		for itemid, item in enumerate(self.items):
			if(item.isExpanded()):
				#find corresponding tableMarking
				marking = self.tableMarkings[itemid]
				#create expansionString
				expandedString = self.interpretDetailFormatString(item)
				newString = "|-- " + expandedString
				#add this string to table at tableindex [markingsLineIndex + markingsLineCount]
				expandIndex = marking[1] + marking[2]
				self.table.insert(expandIndex, newString)

				#we now have added a line to the entry, save that info into markings
				self.recalculateMarkings()

		# newTable = []
		# for index, line in enumerate(self.table):
		# 	newTable.append(line)
		# 	if(index < self.skipLines):
		# 		continue
		# 	for itemid, item in enumerate(self.items):
		# 		if(index - self.skipLines == itemid):
		# 			if(item.isExpanded()):
		# 				#probably add left table seperator ?! "|"
		# 				expandedString = self.interpretDetailFormatString(item)
		# 				newTable.append("|-- " + expandedString)
		# self.table = newTable

	def alignment(self):
		spaces = ""
		#grab tty size (in characters), see https://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python
		rows, columns = os.popen('stty size', 'r').read().split()
		#how long is this table?
		length = 0
		for line in self.table:
			if len(line) > length:
				length = len(line)
		if(self.align == "center"):
			#try to centroid it
			div = (float(columns) / float(length) / 2)
			#print(int(div * length))
			spaces = " " * int(div * length - length/2)
		#add spaces
		for i, line in enumerate(self.table):
			line = spaces + line 
			self.table[i] = line
		#set table attributes 
		self.tableLeft = len(spaces)
		self.tableWidth = length
		self.tableRight = self.tableLeft + self.tableWidth
		self.tableHeight = len(self.table)

	#see https://stackoverflow.com/questions/2330245/python-change-text-color-in-shell
	#http://ascii-table.com/ansi-escape-sequences.php
	def colorText(self, string, fg="WHITE", bg="BLACK", bold=False):
		#find if there is allready a coloring in this string and remove it
		coloredStringContent="\x1b[0m"
		index = string.find(coloredStringContent)
		if(index > 0):
			#remove all these bad things from the allready colored string
			#hacky as fuck ;)
			string = string[8:len(string)-4]
		
		bold = "0"
		if bold:
			bold = "1"
		fg = Color.getFg(fg)
		bg = Color.getBg(bg)
		attrStr = bold + ";" + fg + ";" + bg + "m" + string
		#print(attrStr + "\n")
		return ("\x1b[%s\x1b[0m" % attrStr)		#type(bold etc) ; forground color ; background color 'm' String

	def colorLine(self, line, fg="WHITE", bg="BLACK", bold=False):
		line = self.colorText(line, fg, bg , bold)
		return line

	def colorize(self):
		#split into lines printed
		#markExtended = False

		#overdraw normal table
		for i, line in enumerate(self.table):
			self.table[i] = self.colorLine(line, "WHITE", "BLACK", False)

		#overdraw colored entry by grabbing position in tablemarkings
		#marking[0] == entryID , marking[1] == lineNumber, marking[2] = lineCount
		if(len(self.tableMarkings) > 0):
			marking = self.tableMarkings[self.position]
			#iterate through every line form startIndex in markings[1] to endindex with linecount in markins[2]
			# endindex = startindex + linecount
			for lineIndex in range(marking[1], marking[1] + marking[2]):
				line = self.table[lineIndex]
				line = self.colorLine(line, "WHITE", "RED", False)
				self.table[lineIndex] = line

		
		#for i, line in enumerate(self.table):
		#	#if selected item is reached
		#	if self.position is not -1 and (self.position + self.skipLines) == i:
		#		#if(self.items[self.position].isExpanded()):
		#			#markExtended = True
		#		bgc = "RED"
		#	else:
		#		#if we declared a expanded line before
		#		bgc = "BLACK"
		#		#if(markExtended):
		#		#	markExtended = False
		#		#	bgc = "RED"
		#	#draw line regularly
		#	self.table[i] = self.colorLine(line, "WHITE", bgc, False)



	def interpretFormatKey(self, r):
		key = r[r.find(self.leftValDelim) + len(self.leftValDelim):r.find(self.rightValDelim)]
		if(key is not ""):
			return key

	def interpretMainFormatKeys(self):
		formatKeys = []
		replacers = self.mainFormat.split("|") 	#seperate formats
		for r in replacers: 					#find keys in formatstrings
			key = self.interpretFormatKey(r)
			formatKeys.append(key)
		return formatKeys

	#resolve DetailFormatString for specific item
	def interpretDetailFormatString(self, item):
		expandedStr = ""
		if(self.detailFormat is not ""):
			replacers = self.detailFormat.split("|") 	#seperate formats
			for r in replacers: 
				content = r.split(":") #seperate formats again by key:value
				#check if msg is also a ky, if true, use that keyname as str
				message = self.interpretFormatKey(content[0])
				if(message is ""):
					message = content[0]
				#resolve key name alone
				keystr = content[1]
				key = self.interpretFormatKey(keystr)
				expandedStr += message + ":" + item.get(key) + "    "
		return expandedStr
	#	replacers = self.mainFormat.split("|")
