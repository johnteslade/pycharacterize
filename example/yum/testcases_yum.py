import unittest
import yum

class Test_yum_config_BoolOption(unittest.TestCase):
    
    def test_MyTest_1(self):
    
        print "Starting execution of autogen test harness for yum.config.BoolOption" 
        
        from pycharacterize.object_factory import object_factory
        
        # Object initialiser
        obj_var = yum.config.BoolOption(default=False, parse_default=False)
        
        # Call to parse
        ret = obj_var.parse(s='0')
        expected_return = False
        self.assertEqual(ret, expected_return)
        
        print "Done with execution of autogen test harness for yum.config.BoolOption" 
        
    def test_MyTest_2(self):
    
        print "Starting execution of autogen test harness for yum.config.BoolOption" 
        
        from pycharacterize.object_factory import object_factory
        
        # Object initialiser
        obj_var = yum.config.BoolOption(default=False, parse_default=False)
        
        # Call to parse
        ret = obj_var.parse(s='1')
        expected_return = True
        self.assertEqual(ret, expected_return)
        
        print "Done with execution of autogen test harness for yum.config.BoolOption" 
        
suite = unittest.TestLoader().loadTestsFromTestCase(Test_yum_config_BoolOption)
unittest.TextTestRunner(verbosity=2).run(suite)