
class MyTest:

	def __init__(self):
		self.a = []
		self.b = 1
		self.c = 2

	def add(self, item):
		self.a.append(item)

	def get(self):
		return self.a
	
	def inc(self, val):
		self.b += val
    
	def inc_by_1(self):
		self.inc(1)

	def equal(self):
		return self.b == self.c


