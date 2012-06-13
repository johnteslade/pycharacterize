import bdb
import sys
import linecache
import test_pdb
import mytest


def manipulate_class():

    test_obj = mytest.MyTest()

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


if __name__ == "__main__":
    
    pdb_obj = test_pdb.TestPdb()
   
    pdb_obj.set_class_to_watch("mytest.MyTest")

    pdb_obj.runcall(manipulate_class)

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


   
        
