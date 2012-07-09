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

    def manipulate_given_class(self, class_to_test, class_to_test_str):
        """ Tests the given class using manipulate_class() """

        pdb_obj = test_pdb.TestPdb()
        pdb_obj.set_class_to_watch(class_to_test, class_to_test_str)
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

        self.manipulate_given_class(mytest.MyTest, "mytest.MyTest")
    
    def test_MyTest2(self):

        self.manipulate_given_class(mytest.MyTest2, "mytest.MyTest2")

    def test_MyTest3(self):

        self.manipulate_given_class(mytest.MyTest3, "mytest.MyTest3")

    def test_MyTest4(self):

        self.manipulate_given_class(mytest.MyTest4, "mytest.MyTest4")

if __name__ == '__main__':
    
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

