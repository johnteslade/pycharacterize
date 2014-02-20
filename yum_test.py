import bdb
import sys
import linecache
import pycharacterize 
import yum
import logging




if __name__ == "__main__":
    
    #logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)

    sys.path.insert(0, '/usr/share/yum-cli')
    import yummain

    pych_obj = pycharacterize.runner.Runner()
   
    pych_obj.set_class_to_watch(yum.config.BoolOption, "yum.config.BoolOption")
    #pych_obj.set_class_to_watch(yum.config.IntOption, "yum.config.IntOption")

#    pych_obj.do_runcall(yummain.user_main, ['info', 'firefox'], exit_code=True)
    pych_obj.do_runcall(yummain.user_main, [], exit_code=True)




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


    pych_obj.output_test_code_to_file("testcases_yum.py", backtrace=True)

    print
    print "!!!!!!!!!!!!!!!!!!! RUNNING THE AUTOGEN ----------------"
    print

    exec(test_code)

    print "------ DONe "




   
        
