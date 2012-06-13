
class MyTestBase:

	def __init__(self):
		raise NotImplementedError

	def add(self, item):
		raise NotImplementedError

	def get(self):
		raise NotImplementedError
	
	def inc(self, val):
		raise NotImplementedError
    
	def inc_by_1(self):
		raise NotImplementedError

	def equal(self):
		raise NotImplementedError


class MyTest(MyTestBase):

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


