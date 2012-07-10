from object_state import ObjectState
from object_code_output import ObjectCodeOutput
import logging

class ObjectsList():
    """ Class to hold the objects of interest as they change """
    
    def __init__(self):
        """ Init """

        self.class_of_interest = None # String of class we are interested in
        self.class_of_interest_ref = None # Class references of class we are interested in
        self.object_state_list = [] # List of objects being monitored


    def set_class_to_watch(self, class_name):
        """ Sets the class name to watch for - as a string """
        self.class_of_interest = str(class_name)
        self.class_of_interest_ref = class_name
        

    def is_of_interest(self, class_name, class_name_ref):
        """ Is this class one being watched? """

        #logging.debug("Of iterest in = {} , cmp = {} {}".format(class_name, self.class_of_interest, "__main__." + self.class_of_interest))
        # Sometimes the intested class with be prefixed with __main__ depending on the calling env
        return (self.class_of_interest != None) and (class_name == self.class_of_interest or class_name == "__main__." + self.class_of_interest or (class_name_ref == self.class_of_interest_ref))

    
    def run_finished(self):
        """ Called when the run as finished to clean up """

        logging.debug("Run has finished")

        self.remove_dups()


    def remove_dups(self):
        """ Remove duplicates from object lists """
        for object_state in self.object_state_list:

            logging.debug("State = {}".format(object_state.call_trace))

            if len(filter(lambda x: x.call_trace == object_state.call_trace, self.object_state_list)) > 1:
                print "Found a dupe"


    def _get_object_state(self, obj_id):
        """ Returns the object state of interest """

        matching_id = filter(lambda x: x.id == obj_id, self.object_state_list)
        assert(len(matching_id) <= 1)

        if len(matching_id) == 1:
            return matching_id[0]
        else:
            self.object_state_list.append(ObjectState(self.class_of_interest_ref, obj_id))
            return self.object_state_list[-1]


    def function_call(self, local_vars, func_name):
        """ A call to a function """

        logging.debug("Call from {}".format(id(local_vars['self'])))

        self._get_object_state(id(local_vars['self'])).function_call(local_vars, func_name)


    def function_return(self, local_vars, func_name, stack):
        """ A return from a function """
        
        logging.debug("Return from {}".format(id(local_vars['self'])))

        self._get_object_state(id(local_vars['self'])).function_return(local_vars, func_name, stack)


    def output_test_code(self, **kwarg):
        return ObjectCodeOutput().output_test_code(self.object_state_list, **kwarg)


    def output_test_code_annotated(self):
        return ObjectCodeOutput().output_test_code_annotated(self.object_state_list)


    def call_outstanding(self):
        """ Are any objects still inside a call? """
        return len( filter(lambda x: len(x.call_stack) > 0, self.object_state_list) ) > 0

    
    def get_call_trace(self):
        """ Returns the call trace """

        # TODO figure out what to return here
        return self.object_state_list[0].call_trace



