import bdb
import sys
import linecache
import pycharacterize 
import yum
import logging
import dateutil


def dateutil_test():

    
    import dateutil.parser
 
    p = dateutil.parser.parser()

    a = p.parse("1-Jan-2012")
    print a
    
    a = p.parse("3rd March 1978")
    print a
    
    a = p.parse("23-08-1960")
    print a

#    p1 = dateutil.parser.parser()
#    a1 = p1.parse("1-Jan-2012")
#    print a1
#    
#    p2 = dateutil.parser.parser()
#    a2 = p2.parse("3rd March 1978")
#    print a2
#    
#    p3 = dateutil.parser.parser()
#    a3 = p3.parse("23-08-1960")
#    print a3


if __name__ == "__main__":
  
    dateutil_test()

    #logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)

    sys.path.insert(0, '/usr/share/yum-cli')
    import yummain

    pych_obj = pycharacterize.runner.Runner()

    pych_obj.do_calltrace(dateutil_test)
    

    pych_obj.output_calltrace()
    
    print pych_obj.all_calls.items()
    print pych_obj.class_counts.items()


    # Create tests

    pych_obj = pycharacterize.runner.Runner(step_all=True)
   
    pych_obj.set_class_to_watch(dateutil.parser.parserinfo, "dateutil.parser.parserinfo")

    pych_obj.do_runcall(dateutil_test)


    print
    print "!!!!!!!!!!!!!!!!!!!----------------"
    print

    test_code = pych_obj.output_test_code(backtrace=True)
    print test_code

    print
    print "---------------- All Calls"
    print pych_obj.all_calls.items()
    print pych_obj.class_counts.items()
    print 


    pych_obj.output_test_code_to_file("testcases_dateutil.py", backtrace=True)

    print
    print "!!!!!!!!!!!!!!!!!!! RUNNING THE AUTOGEN ----------------"
    print

    exec(test_code)

    print "------ DONe "




   
        
