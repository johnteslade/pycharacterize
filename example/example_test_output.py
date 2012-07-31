import unittest
import class_ut

class Test_class_ut_MyTest(unittest.TestCase):
   
   def test_MyTest_1(self):
   
     print "Starting execution of autogen test harness for class_ut.MyTest" 
     
     from pycharacterize.object_factory import object_factory
     
     # Object initialiser
     obj_var = class_ut.MyTest()
     
     # Call to get_for_a
     ret = obj_var.get_for_a()
     expected_return = 4
     self.assertEqual(ret, expected_return)
     
     # Call to add_a
     obj_var.add_a(item=4)
     
     # Call to get_a
     ret = obj_var.get_a()
     expected_return = 1
     self.assertEqual(ret, expected_return)
     
     # Call to equal
     ret = obj_var.equal()
     expected_return = False
     self.assertEqual(ret, expected_return)
     
     # Attributes changed directly
     obj_var.c = 4
     
     # Call to inc_by_1
     obj_var.inc_by_1()
     
     # Call to equal
     ret = obj_var.equal()
     expected_return = False
     self.assertEqual(ret, expected_return)
     
     # Call to inc
     obj_var.inc(val=2)
     
     # Call to equal
     ret = obj_var.equal()
     expected_return = True
     self.assertEqual(ret, expected_return)
     
     print "Done with execution of autogen test harness for class_ut.MyTest" 
     
suite = unittest.TestLoader().loadTestsFromTestCase(Test_class_ut_MyTest)
unittest.TextTestRunner(verbosity=2).run(suite)