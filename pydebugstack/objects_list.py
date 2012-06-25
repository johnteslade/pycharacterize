from object_state import ObjectState
from object_code_output import ObjectCodeOutput
import logging

class ObjectsList():
    """ Class to hold the objects of interest as they change """
    
    def __init__(self):
        """ Init """

        self.class_of_interest = None # String of class we are interested in
        self.class_of_interest_ref = None # Class references of class we are interested in
        self.object_state = None # The object - TODO this needs to become a list


    def set_class_to_watch(self, class_name):
        """ Sets the class name to watch for - as a string """
        self.class_of_interest = str(class_name)
        self.class_of_interest_ref = class_name
        self.object_state = ObjectState(class_name) # The object - TODO this needs to become a list
    
        self.obj_id = None # id of object TODO remove when multiple are supported

    def is_of_interest(self, class_name, class_name_ref):
        """ Is this class one being watched? """

        #logging.debug("Of iterest in = {} , cmp = {} {}".format(class_name, self.class_of_interest, "__main__." + self.class_of_interest))
        # Sometimes the intested class with be prefixed with __main__ depending on the calling env
        return (self.class_of_interest != None) and (class_name == self.class_of_interest or class_name == "__main__." + self.class_of_interest or (class_name_ref == self.class_of_interest_ref))

        
    def function_call(self, local_vars, func_name):
        """ A call to a function """

        logging.debug("Call from {}".format(id(local_vars['self'])))

        if self.obj_id == None:
            self.obj_id = id(local_vars['self'])
        else:
            assert(self.obj_id == id(local_vars['self']))

        self.object_state.function_call(local_vars, func_name)

    def function_return(self, local_vars, func_name):
        """ A return from a function """
        
        logging.debug("Return from {}".format(id(local_vars['self'])))

        if self.obj_id == None:
            self.obj_id = id(local_vars['self'])
        else:
            assert(self.obj_id == id(local_vars['self']))

        self.object_state.function_return(local_vars, func_name)

    def output_test_code(self):
        return ObjectCodeOutput().output_test_code(self.object_state)


    def call_outstanding(self):
        """ Are we still inside a call? """
        return len(self.object_state.call_stack) > 0

    
    def get_call_trace(self):
        """ Returns the call trace """

        return self.object_state.call_trace



