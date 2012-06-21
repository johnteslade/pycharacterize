import unittest
import bdb
import sys
import linecache
import test_pdb
import logging

class MyTestBase:

    def add_a(self, item):
        raise NotImplementedError

    def get_a(self):
        raise NotImplementedError
    
    def get_for_a(self):
        raise NotImplementedError

    def inc(self, val):
        raise NotImplementedError
    
    def inc_by_1(self):
        raise NotImplementedError

    def equal(self):
        raise NotImplementedError

class MyTest(MyTestBase):
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


class MyTest2(MyTestBase):
    """ Class that has no main constructor """

    def add_a(self, item):
        pass

    def get_a(self):
        return 1

    def get_for_a(self):
        return 4

    def inc(self, val):
        return 99 + val
    
    def inc_by_1(self):
        return self.inc(1)

    def equal(self):
        return True


class MyTest3(MyTest):
    """ Class that has a parent """

    def inc(self, val):
        self.b += (val * 100)


class MyTest4(MyTest):
    """ Class that returns objects """

    def get_for_a(self):
        return AnObject()


class AnObject():
    """ Generic class that can be passed around """

    def __init__(self, x=1, y=10, z=100):
        self.x = x
        self.y = y
        self.z = z


def manipulate_class(class_in):
    """ This function calls the specified class so behaviour is created """

    test_obj = class_in()

    item_for_a = test_obj.get_for_a()
    print "manipulate_class: {}".format(item_for_a)

    test_obj.add_a(item_for_a)
    out = test_obj.get_a()
    print "manipulate_class: {}".format(out)

    out = test_obj.equal()
    print "manipulate_class: {}".format(out)
   
    test_obj.c = 3

    test_obj.inc_by_1()
    out = test_obj.equal()
    print "manipulate_class: {}".format(out)

    test_obj.inc(3)
    out = test_obj.equal()
    print "manipulate_class: {}".format(out)

    exit()


