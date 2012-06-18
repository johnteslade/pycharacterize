import bdb
import sys
import linecache
import test_pdb
import mytest
import logging

if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.INFO)

    pdb_obj = test_pdb.TestPdb()
    pdb_obj.set_class_to_watch("mytest.MyTest4")
    pdb_obj.do_runcall(mytest.manipulate_class, mytest.MyTest4)

    print
    print "!!!!!!!!!!!!!!!!!!!----------------"
    print

    print pdb_obj.call_trace
    
    print

    test_code = pdb_obj.output_test_code()
    print test_code

    print
    print "---------------- All Calls"
    print pdb_obj.all_calls.items()
    print pdb_obj.class_counts.items()
    print 



    print
    print "!!!!!!!!!!!!!!!!!!! RUNNING THE AUTOGEN ----------------"
    print

    exec(test_code)

    print "------ DONe "


   
        
