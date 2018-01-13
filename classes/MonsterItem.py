

class MonsterItem:

	leftValDelim = "$("
	rightValDelim = ")$"

	leftInjectDelim = ".INJ["
	rightInjectDelim = "]INJ."

	def __init__(self, id, obj, relevantKeys, format):
		self.id = id   
		self.data = obj.__dict__
		self.format = format
		self.relevantKeys = relevantKeys

		#self.interpretKeys()
		#self.formatData()


	def get(self, header):
		for key in self.relevantKeys:
			if header is key:
				return self.data[key]

	def getData(self, keys):
		data = []
		for key in keys:
			data.append(self.data[key])
		return data

	# def interpretKeys(self):
	# 	formatKeys = []

	# 	#seperate formats
	# 	replacers = self.format.split("|")
	# 	#find keys in formatstrings
	# 	for r in replacers:
	# 		for key,val in self.data.iteritems():
	# 			c1 = r.find(self.leftValDelim) + len(self.leftValDelim)
	# 			c2 = r.find(self.rightValDelim)
	# 			delim = r[c1:c2]
	# 			#if(c > 0 and key == r[c:]):
	# 			if(key == delim):
	# 				#this is a usable key attribute
	# 				formatKeys.append(key)
	# 				break
	# 	self.fkeys = formatKeys


	# def injectInsertSymbols(self):
	# 	pre = []
	# 	post = []
	# 	replacers = self.format.split("|")
	# 	for r in replacers:
	# 		stringL = ""
	# 		stringR = ""
	# 		c = r.find(self.leftInjectDelim)
	# 		if(c != -1):
	# 			delim = r[c + len(self.leftInjectDelim):r.find(self.rightInjectDelim)]
	# 			if(delim is not ""):
	# 				#decide whether the command is left or right of val
	# 				side = "R"
	# 				if (r.find(self.leftValDelim) > c):
	# 					side = "L"
	# 				delim = delim.split(",")
	# 				string = delim[0]
	# 				count = int(delim[1])
	# 				strings = string * count
	# 				if(side is "L"):
	# 					stringL = strings
	# 				else:
	# 					stringR = strings
	# 			#after if(delim is not ""):
	# 		pre.append(stringL)
	# 		post.append(stringR)

	# 	print("___________________________________________")
	# 	print(pre)
	# 	print(post)
	# 	return (pre, post)

	# def formatData(self):
	# 	pre, post = self.injectInsertSymbols()

	# 	self.fdata = []
	# 	for i, key in enumerate(self.fkeys):
	# 		self.fdata.append(pre[i] + self.data[key] + post[i])

	# def attrInFormat(self):
	# 	return False

	def __str__(self):
		return "foo"




