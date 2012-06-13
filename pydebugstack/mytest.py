import unittest
import bdb
import sys
import linecache
import test_pdb
import logging

class MyTestBase:

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
    """ test """

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

class MyTest2(MyTestBase):
    """ Class that has no main constructor """

    def add(self, item):
        pass

    def get(self):
        return 1
    
    def inc(self, val):
        return 99 + val
    
    def inc_by_1(self):
        return self.inc(1)

    def equal(self):
        return True


def manipulate_class(class_in):
    """ This function calls the specified class so behaviour is created """

    test_obj = class_in()

    test_obj.add(4)
    out = test_obj.get()
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

class Test_test_Pdb(unittest.TestCase):
    
    def setUp(self):
        pass

    def manipulate_given_class(self, class_to_test, class_to_watch_str):
        """ Tests the given class using manipulate_class() """

        pdb_obj = test_pdb.TestPdb()
        pdb_obj.set_class_to_watch(class_to_watch_str)
        pdb_obj.do_runcall(manipulate_class, class_to_test)

        # There must be a call trace
        self.assertTrue(len(pdb_obj.call_trace) > 0)

        # Check we have some test code output
        test_code = pdb_obj.output_test_code()
        logging.debug(test_code)
        self.assertTrue(test_code > 0)

        # Execute the code - this will raise exceptions if wrong
        exec(test_code)

    def test_MyTest(self):

        self.manipulate_given_class(MyTest, "MyTest")
    
    def test_MyTest2(self):

        self.manipulate_given_class(MyTest2, "MyTest2")

if __name__ == '__main__':
    
    #logging.basicConfig(level=logging.DEBUG)
    unittest.main()

