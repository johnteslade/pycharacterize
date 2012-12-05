import unittest
import bdb
import sys
import linecache
import logging
import class_ut

# Modify paths so import pycharacterize works
sys.path.append("../")
sys.path.append(".")

import pycharacterize 


def do_stuff():
    """ This function calls the specified class so behaviour is created """

    test_obj = class_ut.MyTest()

    step_1(test_obj)
    step_2(test_obj)


def step_1(test_obj):
    
    item_for_a = test_obj.get_for_a()

    test_obj.add_a(item_for_a)
    out = test_obj.get_a()


def step_2(test_obj):

    step_2a(test_obj)

    test_obj.inc_by_1()
    out = test_obj.equal()

    test_obj.inc(2)
    out = test_obj.equal()


def step_2a(test_obj):

    out = test_obj.equal()
   
    test_obj.c = 4


if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.INFO)

    pdb_obj = pycharacterize.runner.Runner(step_all=False)

    pdb_obj.set_class_to_watch(class_ut.MyTest, "class_ut.MyTest")
    pdb_obj.do_runcall(do_stuff)

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

    pdb_obj.output_test_code_to_file("./example_test_output.py")

    print
    print "!!!!!!!!!!!!!!!!!!! RUNNING THE AUTOGEN ----------------"
    print

    exec(test_code)

    print "------ DONe "




