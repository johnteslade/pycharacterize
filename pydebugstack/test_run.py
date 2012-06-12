import bdb
import sys
import linecache

from mytest import MyTest



def manipulate_class():

    test_obj = MyTest()

    test_obj.add(4)
    out = test_obj.get()
    print out

    out = test_obj.equal()
    print out
    
    test_obj.inc()
    out = test_obj.equal()
    print out

    test_obj.inc()
    out = test_obj.equal()
    print out    

if __name__ == "__main__":

    bdb_obj = bdb.Bdb()
    
    filename = "mytest.py"

    lines = linecache.getlines(filename)
    print "file has {} lines".format(len(lines))

    print "Breaks = {}".format(bdb_obj.get_file_breaks(filename))

    for i in xrange(len(lines)):
        bdb_obj.set_break(filename, i)
    
    print "Breaks = {}".format(bdb_obj.get_file_breaks(filename))

    bdb_obj.run(manipulate_class())
    
    print "Breaks = {}".format(bdb_obj.get_file_breaks(filename))
    
   
        
