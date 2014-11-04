import bdb
import sys
import linecache
import pycharacterize
import logging


def ecdsa_test():

    from ecdsa import SigningKey
    from ecdsa.ellipticcurve import CurveFp, Point
    c = CurveFp( 23, 1, 1 )
    p1 = Point( c, 3, 10 )
    p2 = Point( c, 9, 7 )
    p3 = p1 + p2
    if p3.x() != 17 or p3.y() != 20:
        raise Exception("Failure: should give (%d,%d)." % ( x3, y3 ))
    #sk = SigningKey.generate() # uses NIST192p
    #vk = sk.get_verifying_key()
    #signature = sk.sign("message")
    #assert vk.verify(signature, "message")

if __name__ == "__main__":

    ecdsa_test()

#    logging.basicConfig(level=logging.WARNING)
    logging.basicConfig(level=logging.DEBUG)

#    pych_obj = pycharacterize.runner.Runner()
#
#    pych_obj.do_calltrace(ecdsa_test)
#
#    pych_obj.output_calltrace()
#
#    print pych_obj.all_calls.items()
#    print pych_obj.class_counts.items()
#
#    exit()


    # Create tests

    pych_obj = pycharacterize.runner.Runner(step_all=True)

    import ecdsa
    pych_obj.set_class_to_watch(ecdsa.ellipticcurve.Point, "ecdsa.ellipticcurve.Point")

    pych_obj.do_runcall(ecdsa_test)


    print
    print "!!!!!!!!!!!!!!!!!!!----------------"
    print

    test_code = pych_obj.output_test_code(backtrace=True)
    #print test_code

    print
    print "---------------- All Calls"
    print pych_obj.all_calls.items()
    print pych_obj.class_counts.items()
    print


    pych_obj.output_test_code_to_file("testcases_ecdsa.py", backtrace=True)

    print
    print "!!!!!!!!!!!!!!!!!!! RUNNING THE AUTOGEN ----------------"
    print

#    exec(test_code)

    print "------ DONe "






