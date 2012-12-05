
class MyTest(object):
    """ test """

    def __init__(self):
        self.a = []
        self.b = 1
        self.c = 2

    def add_a(self, item):
        self.a.append(item)

    def get_a(self):
        return len(self.a)

    def get_for_a(self):
        return 4

    def inc(self, val):
        """ Inc func """
        self.b += val
    
    def inc_by_1(self):
        self.inc(1)

    def equal(self):
        return self.b == self.c


