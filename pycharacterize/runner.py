"""Main runner code"""

"""This is a modified version of PDB - and under the same license """

import bdb
import cmd
import inspect
import linecache
import logging
import os
import pprint
import re
import sys

from collections import defaultdict
from repr import Repr

from objects_list import ObjectsList



# Create a custom safe Repr instance and increase its maxstring.
# The default of 30 truncates error messages too easily.
_repr = Repr()
_repr.maxstring = 200
_saferepr = _repr.repr


class TestPdb(bdb.Bdb):

    def __init__(self, completekey='tab', skip=None, step_all=False):
        bdb.Bdb.__init__(self, skip=skip)
        
        self._wait_for_mainpyfile = 0

        self.step_all = step_all # Should we step through all execution

        self.class_of_interest = None # Class name we are interested in
        self.all_calls = defaultdict(lambda: defaultdict(int)) # All functions calls found
        self.class_counts = defaultdict(int) # Counts methods in each class found

        self.objects_list = ObjectsList() # List of objects

        self.filename_of_interest = None # The filename we are looking for

        # Reset all vars
        self.reset()
        self.forget()


    def forget(self):
        self.lineno = None
        self.stack = []
        self.curindex = 0
        self.curframe = None

    def setup(self, f, t):
        self.forget()
        self.stack, self.curindex = self.get_stack(f, t)
        self.curframe = self.stack[self.curindex][0]
        # The f_locals dictionary is updated from the actual frame
        # locals whenever the .f_locals accessor is called, so we
        # cache it here to ensure that modifications are not overwritten.
        self.curframe_locals = self.curframe.f_locals
        

    def do_runcall(self, *args, **kwds):
        """ Makes the function call """

        # Run but catch if the program exits - we still need to keep executing
        try:
            self.runcall(*args, **kwds)
        except SystemExit:
            logging.debug("Caller raised SystemExit")
        finally:
            # Clear breaks
            # This appears to be a bug in bdb - if they are not cleared they are still active in 
            # the next instance of BDB
            self.clear_all_breaks()

            # Finish objects
            self.objects_list.run_finished()

    # Override Bdb methods

    def user_call(self, frame, argument_list):
        """This method is called when there is the remote possibility
        that we ever need to stop in this function."""
        if self._wait_for_mainpyfile:
            return
        if self.stop_here(frame):
            logging.debug("Call")
            self.interaction(frame, None, func_call=True)

    def user_line(self, frame):
        """This function is called when we stop or break at this line."""
        if self._wait_for_mainpyfile:
            if frame.f_lineno<= 0:
                return
            self._wait_for_mainpyfile = 0
        logging.debug("Line {} {}".format(frame.f_code.co_filename, frame.f_lineno))
        self.interaction(frame, None, func_call=(not self.step_all))

    def user_return(self, frame, return_value):
        """This function is called when a return trap is set here."""
        if self._wait_for_mainpyfile:
            return
        frame.f_locals['__return__'] = return_value
        logging.debug("Return")
        self.interaction(frame, None, func_return=True)

    def user_exception(self, frame, exc_info):
        """This function is called if an exception occurs,
        but only if we are to stop at or just below this level."""
        if self._wait_for_mainpyfile:
            return
        exc_type, exc_value, exc_traceback = exc_info
        frame.f_locals['__exception__'] = exc_type, exc_value
        if type(exc_type) == type(''):
            exc_type_name = exc_type
        else: exc_type_name = exc_type.__name__
        logging.debug("user_exception")
        logging.debug(exc_type_name + ':' + _saferepr(exc_value))
        self.interaction(frame, exc_traceback)


    def set_class_to_watch(self, class_name, class_name_str):
        """ Sets the class name to watch for - as a string """

        if type(class_name_str) != str:
            raise Exception("Class name must be a string")

        # Save the class name
        self.objects_list.set_class_to_watch(class_name_str)

        # Get list of class functions and set breakpoints
        class_functions = self.find_class_functions(class_name)
        self.filename_of_interest = class_functions[0]['filename']
        
        if not self.step_all:
            self.set_breakpoints(class_functions)
        
        print "Breaks = {}".format(self.get_all_breaks())


    def set_breakpoints(self, class_functions):
        """ Sets breakpoints on all functions """

        for funcs in class_functions:

            err = self.set_break(funcs['filename'], funcs['line'], False, None, funcs['name'])
            if err: 
                print '***', err
            else:
                bp = self.get_breaks(funcs['filename'], funcs['line'])[-1]
                print "Breakpoint %d at %s:%d - for func %s" % (bp.number, bp.file, bp.line, funcs['name'])

        print "now {} breaks".format(self.get_all_breaks())


    def find_class_functions(self, class_name):
        """ Finds filename and lineno for all functions in the class """

        func_details = []

        # Look at all class attributes
        for attr_name in dir(class_name):

            attr = getattr(class_name, attr_name)

            # If a function then save
            if 'im_func' in dir(attr) and (attr.func_code.co_name.startswith("__") or not(attr.func_code.co_name.startswith("_"))):

                func_details.append({'name': attr.func_code.co_name, 'line': attr.func_code.co_firstlineno, 'filename': attr.func_code.co_filename})

        return func_details


    def interaction(self, frame, traceback, func_call=False, func_return=False):
        """ Called when there is an interaction to deal with """

        self.setup(frame, traceback)
        #self.print_stack_entry(self.stack[self.curindex])
       
        #logging.debug("Class = {}, Func = {}, call = {}, return = {}".format("", self.stack[self.curindex][0].f_code.co_name, func_call, func_return))

        (args, varargs, keywords, local_vars) = inspect.getargvalues(frame)  
        #print "a = {}".format(args)
        #print "v = {}".format(varargs)
        #print "k = {}".format(keywords)
        #print "l = {}".format(local_vars)
       
        # Look for the class
        if 'self' in local_vars:
       
            class_name = local_vars['self'].__class__.__module__ + "." + local_vars['self'].__class__.__name__ 

            #logging.debug("Mod = {}, Class = {}".format(local_vars['self'].__class__.__module__, local_vars['self'].__class__.__name__))

            #logging.debug("Class = {}, Func = {}, call = {}, return = {}".format(class_name, self.stack[self.curindex][0].f_code.co_name, func_call, func_return))

            # Save all functions we encounter
            if func_call:
                self.all_calls[class_name][self.stack[self.curindex][0].f_code.co_name] += 1
                self.class_counts[class_name] += 1

            # Class we are interested in? 
            if self.objects_list.is_of_interest(class_name, local_vars['self'].__class__):
            
                logging.debug("Of interest --- Class = {}, Func = {}, call = {}, return = {}".format(class_name, self.stack[self.curindex][0].f_code.co_name, func_call, func_return))
            
                if func_call:
                    self.objects_list.function_call(local_vars, self.stack[self.curindex][0].f_code.co_name)

                # Save the details of the function call
                if func_return:
                    self.objects_list.function_return(local_vars, self.stack[self.curindex][0].f_code.co_name, self.stack)
                 

        #logging.debug("")
        #logging.debug("--------------")

        # Determine the step mode
        if self.step_all:
            self.set_step()
        else:
            # If we entered a function then wait for return
            if self.objects_list.call_outstanding():
                logging.debug("Call outstanding - do return")
                self.set_return(self.curframe)
            else:
                self.set_continue()

        self.forget()

    
    def output_test_code(self, **kwargs):
        """ Output the test code """

        return self.objects_list.output_test_code(**kwargs)
 

    def output_test_code_annotated(self, **kwargs):

        return self.objects_list.output_test_code_annotated(**kwargs)
    
 
    def output_test_code_to_file(self, filename, **kwargs):

        fw = open(filename, 'w')
        fw.write(self.objects_list.output_test_code(**kwargs))
        fw.close()

