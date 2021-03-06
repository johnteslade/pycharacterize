import mytest
import unittest
import bdb
import sys
import linecache

# Modify paths so import pycharacterize works
sys.path.append("../")
sys.path.append(".")

import pycharacterize
import logging


class Test_test_Pdb(unittest.TestCase):
    
    def setUp(self):
        pass

    def manipulate_given_class(self, class_to_test, class_to_test_str, manipulate_func=mytest.manipulate_class, step_all=False):
        """ Tests the given class using manipulate_class() """

        pych_obj = pycharacterize.Runner(step_all=step_all)
        pych_obj.set_class_to_watch(class_to_test, class_to_test_str)
        pych_obj.do_runcall(manipulate_func, class_to_test)

        # There must be a call trace
        self.assertTrue(len(pych_obj.objects_list.get_call_trace()) > 0)

        # Check we have some test code output
        test_code = pych_obj.output_test_code()
        logging.debug(test_code)
        self.assertTrue(test_code > 0)

        # Execute the code - this will raise exceptions if wrong
        exec(test_code)

    def test_MyTest(self):

        self.manipulate_given_class(mytest.MyTest, "mytest.MyTest")
    
    def test_MyTest2(self):

        self.manipulate_given_class(mytest.MyTest2, "mytest.MyTest2")

    def test_MyTest3(self):

        self.manipulate_given_class(mytest.MyTest3, "mytest.MyTest3")

    def test_MyTest4(self):

        self.manipulate_given_class(mytest.MyTest4, "mytest.MyTest4")

    def test_MyTest4_double(self):

        self.manipulate_given_class(mytest.MyTest4, "mytest.MyTest4", mytest.manipulate_class_double)

    def test_MyTest_steapall(self):
        
        self.manipulate_given_class(mytest.MyTest, "mytest.MyTest", step_all=True)


if __name__ == '__main__':
    
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

