import bdb
import sys
import linecache
import test_pdb
import mytest
import logging

import jsonpickle
from samples import Thing

def jsonpickle_main():

 
     
    # Create an object.
    obj = Thing('A String')
    print obj.name
     
    # Use jsonpickle to transform the object into a JSON string.
    pickled = jsonpickle.encode(obj)
    print pickled
     
    # Use jsonpickle to recreate a Python object from a JSON string
    unpickled = jsonpickle.decode(pickled)
    print unpickled.name
     


if __name__ == "__main__":
    
    #logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)

    pych_obj = test_pdb.Runner()
   
    pych_obj.set_class_to_watch(jsonpickle.pickler.Pickler, "jsonpickle.pickler.Pickler")

    pych_obj.do_runcall(jsonpickle_main)




    print
    print "!!!!!!!!!!!!!!!!!!!----------------"
    print

    test_code = pych_obj.output_test_code()
    print test_code

    print
    print "---------------- All Calls"
    print pych_obj.all_calls.items()
    print pych_obj.class_counts.items()
    print 



    print
    print "!!!!!!!!!!!!!!!!!!! RUNNING THE AUTOGEN ----------------"
    print

    exec(test_code)

    print "------ DONe "




   
        
