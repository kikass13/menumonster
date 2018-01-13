
# Foreground colors
# 30	Black
# 31	Red
# 32	Green
# 33	Yellow
# 34	Blue
# 35	Magenta
# 36	Cyan
# 37	White 

# Background colors
# 40	Black
# 41	Red
# 42	Green
# 43	Yellow
# 44	Blue
# 45	Magenta
# 46	Cyan
# 47	White 

class Color:

	def __init__(self):
		pass

	@staticmethod
	def getFg(color):
		code = 30
		color = color.lower()
		if(color == "black"):
			code = 30
		elif(color == "red"):
			code = 31
		elif(color == "green"):
			code = 32
		elif(color == "yellow"):
			code = 33
		elif(color == "blue"):
			code = 34
		elif(color == "magenta"):
			code = 35
		elif(color == "cyan"):
			code = 36
		elif(color == "white"):
			code = 37
		return str(code)

	@staticmethod
	def getBg(color):
		code = 40
		color = color.lower()
		if(color == "black"):
			#black background is actually grey ... so we dont want to return anyrhing usefull
			code = ""
		elif(color == "red"):
			code = 41
		elif(color == "green"):
			code = 42
		elif(color == "yellow"):
			code = 43
		elif(color == "blue"):
			code = 44
		elif(color == "magenta"):
			code = 45
		elif(color == "cyan"):
			code = 46
		elif(color == "white"):
			code = 47
		return str(code)