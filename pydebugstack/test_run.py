import bdb
import sys
import linecache
import test_pdb
import mytest
import logging

if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.INFO)

    pdb_obj = test_pdb.TestPdb(step_all=False)

    class_to_test = mytest.MyTest4 

    pdb_obj.set_class_to_watch(class_to_test)
    pdb_obj.do_runcall(mytest.manipulate_class, class_to_test)

    print
    print "---------------- All Calls"
    print pdb_obj.all_calls.items()
    print pdb_obj.class_counts.items()
    print 


    print
    print "!!!!!!!!!!!!!!!!!!!----------------"
    print

    test_code = pdb_obj.output_test_code()
    print test_code


    print
    print "!!!!!!!!!!!!!!!!!!! RUNNING THE AUTOGEN ----------------"
    print

    exec(test_code)

    print "------ DONe "


   
        
