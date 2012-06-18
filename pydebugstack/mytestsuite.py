import mytest
import unittest
import bdb
import sys
import linecache
import test_pdb
import logging


class Test_test_Pdb(unittest.TestCase):
    
    def setUp(self):
        pass

    def manipulate_given_class(self, class_to_test, step_all_in):
        """ Tests the given class using manipulate_class() """

        pdb_obj = test_pdb.TestPdb(step_all=step_all_in)
        pdb_obj.set_class_to_watch(class_to_test)
        pdb_obj.do_runcall(mytest.manipulate_class, class_to_test)

        # There must be a call trace
        self.assertTrue(len(pdb_obj.objects_list.get_call_trace()) > 0)

        # Check we have some test code output
        test_code = pdb_obj.output_test_code()
        logging.debug(test_code)
        self.assertTrue(test_code > 0)

        # Execute the code - this will raise exceptions if wrong
        exec(test_code)

    def test_MyTest(self):

        self.manipulate_given_class(mytest.MyTest, True)
    
    def test_MyTest2(self):

        self.manipulate_given_class(mytest.MyTest2, True)

    def test_MyTest3(self):

        self.manipulate_given_class(mytest.MyTest3, True)

    def test_MyTest4(self):

        self.manipulate_given_class(mytest.MyTest4, True)

if __name__ == '__main__':
    
    #logging.basicConfig(level=logging.DEBUG)
    unittest.main()

