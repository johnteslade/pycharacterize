import bdb
import sys
import linecache
import test_pdb
import mytest


def manipulate_class():

    test_obj = mytest.MyTest()

    test_obj.add(4)
    out = test_obj.get()
    print out

    out = test_obj.equal()
    print out
    
    test_obj.inc()
    out = test_obj.equal()
    print out

    test_obj.inc(3)
    out = test_obj.equal()
    print out    

def  autogen_test_code():
    """ Copy this in from the code """

    obj_var = mytest.MyTest()
    obj_var.add(item=4)
    ret = obj_var.get()
    assert ret == [4]
    obj_var.equal()
    obj_var.inc(val=1)
    ret = obj_var.equal()
    assert ret == True
    obj_var.inc(val=3)
    obj_var.equal()
        


if __name__ == "__main__":

    pdb_obj = test_pdb.TestPdb()
   
    pdb_obj.set_class_to_watch("mytest.MyTest")

    pdb_obj.runcall(manipulate_class)

    print
    print "!!!!!!!!!!!!!!!!!!!----------------"
    print

    print pdb_obj.call_trace
    
    print

    pdb_obj.output_test_code()



    print
    print "!!!!!!!!!!!!!!!!!!! RUNNING THE AUTOGEN ----------------"
    print

    autogen_test_code()

    print "------ DONe "

#    bdb_obj = bdb.Bdb()
#    
#    filename = "mytest.py"
#
#    lines = linecache.getlines(filename)
#    print "file has {} lines".format(len(lines))
#
#    print "Breaks = {}".format(bdb_obj.get_file_breaks(filename))
#
#    for i in xrange(len(lines)):
#        bdb_obj.set_break(filename, i)
#    
#    print "Breaks = {}".format(bdb_obj.get_file_breaks(filename))
#
#    bdb_obj.set_trace()
#
#    bdb_obj.run(manipulate_class())
#    
#    print "Breaks = {}".format(bdb_obj.get_file_breaks(filename))
    
   
        
