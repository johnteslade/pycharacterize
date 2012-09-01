import bdb
import sys
import linecache
import pycharacterize 
import yum
import logging


def dateutil_test():

    
    import dateutil.parser

    p = dateutil.parser.parser()

    a = p.parse("1-Jan-2012")

    print a


if __name__ == "__main__":
   
    #logging.basicConfig(level=logging.INFO)
    #logging.basicConfig(level=logging.DEBUG)

    sys.path.insert(0, '/usr/share/yum-cli')
    import yummain

    pdb_obj = pycharacterize.runner.TestPdb()

    pdb_obj.do_calltrace(dateutil_test)
    
    print pdb_obj.all_calls.items()
    print pdb_obj.class_counts.items()

    exit()


   
    pdb_obj.set_class_to_watch(yum.config.BoolOption, "yum.config.BoolOption")

#    pdb_obj.do_runcall(yummain.user_main, ['info', 'firefox'], exit_code=True)
    pdb_obj.do_runcall(yummain.user_main, [], exit_code=True)




    print
    print "!!!!!!!!!!!!!!!!!!!----------------"
    print

    test_code = pdb_obj.output_test_code(backtrace=True)
    print test_code

    print
    print "---------------- All Calls"
    print pdb_obj.all_calls.items()
    print pdb_obj.class_counts.items()
    print 


    pdb_obj.output_test_code_to_file("testcases_yum.py", backtrace=True)

    print
    print "!!!!!!!!!!!!!!!!!!! RUNNING THE AUTOGEN ----------------"
    print

    exec(test_code)

    print "------ DONe "




   
        
