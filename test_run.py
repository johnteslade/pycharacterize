import bdb
import sys
import linecache
import pycharacterize 
from tests import mytest
import tests
import logging

if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.INFO)

    pdb_obj = pycharacterize.runner.Runner(step_all=False)

    pdb_obj.set_class_to_watch(mytest.MyTest4, "tests.mytest.MyTest4")
    pdb_obj.do_runcall(mytest.manipulate_class, mytest.MyTest4)

    print
    print "---------------- All Calls"
    print pdb_obj.all_calls.items()
    print pdb_obj.class_counts.items()
    print 


    print
    print "!!!!!!!!!!!!!!!!!!!----------------"
    print

    test_code = pdb_obj.output_test_code(backtrace=True)
    print test_code

    pdb_obj.output_test_code_to_file("test_MyTest4.py", backtrace=True)

    print
    print "!!!!!!!!!!!!!!!!!!! RUNNING THE AUTOGEN ----------------"
    print

    exec(test_code)

    print "------ DONe "


   
        
