import bdb
import sys
import linecache
import test_pdb
import mytest
import yum
import logging


logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    
    sys.path.insert(0, '/usr/share/yum-cli')
    import yummain

    pdb_obj = test_pdb.TestPdb()
   
    #pdb_obj.set_class_to_watch("mytest.MyTest")

    pdb_obj.runcall(yummain.user_main, ['info', 'firefox'], exit_code=True)




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




   
        
