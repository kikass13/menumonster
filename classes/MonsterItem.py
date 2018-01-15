

class MonsterItem:

	leftValDelim = "$("
	rightValDelim = ")$"

	leftInjectDelim = ".INJ["
	rightInjectDelim = "]INJ."

	def __init__(self, id, obj):
		self.id = id   
		self.data = obj.__dict__
		self.expanded = False

	def get(self, header):
		return self.data[header]

	def isExpanded(self):
		return(self.expanded)

	def expand(self):
		self.expanded = True

	def contract(self):
		self.expanded = False


	def search(self, searchstring):
		for key, val in self.data.iteritems():
			if(key.find(searchstring) is not -1 or str(val).find(searchstring) is not -1):
				return True
		return False