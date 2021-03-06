from object_state import ObjectState
from object_code_output import ObjectCodeOutput
import logging

class ObjectsList(object):
    """ Class to hold the objects of interest as they change """

    def __init__(self):
        """ Init """

        self.class_of_interest = None # String of class we are interested in
        self.class_of_interest_ref = None # Class references of class we are interested in
        self.object_state_list = [] # List of objects being monitored
        self.func_names = [] # List of object functions


    def set_class_to_watch(self, class_name, func_names):
        """ Sets the class name to watch for - as a string """
        self.class_of_interest = str(class_name)
        self.class_of_interest_ref = class_name
        self.func_names = func_names


    def is_of_interest(self, class_name, class_name_ref):
        """ Is this class one being watched? """

        #logging.debug("Of iterest in = {} , cmp = {} {}".format(class_name, self.class_of_interest, "__main__." + self.class_of_interest))
        # Sometimes the intested class with be prefixed with __main__ depending on the calling env
        return (self.class_of_interest != None) and (class_name == self.class_of_interest or class_name == "__main__." + self.class_of_interest or (class_name_ref == self.class_of_interest_ref))


    def run_finished(self):
        """ Called when the run as finished to clean up """

        logging.debug("Run has finished")

        self.remove_bad_tests()
        self.remove_dups()


    def remove_bad_tests(self):
        """ Removes any bad calls """

        bad_tests = []

        for object_state in self.object_state_list:

            # Find states where there is an constructor but not calls to it
            if ('__init__' in self.func_names) and len(filter(lambda x: x['type'] == 'func_call' and x['func'] == "__init__", object_state.call_trace)) == 0:
                print "Found bad test: {}".format(object_state.call_trace)
                bad_tests.append(object_state)

        logging.debug("Found {} bad tests".format(len(set(bad_tests))))

        for bad in bad_tests:
            self.object_state_list.remove(bad)


    def remove_dups(self):
        """ Remove duplicates from object lists """

        dupe_tests = []

        for x in xrange(len(self.object_state_list)):

            for y in xrange(x + 1, len(self.object_state_list)):

                s1 = self.object_state_list[x].call_trace
                s2 = self.object_state_list[y].call_trace

                if self.equal_call_traces(s1, s2):
                    dupe_tests.append(self.object_state_list[y])

        logging.debug("Found {} duplicate tests".format(len(set(dupe_tests))))

        for bad in set(dupe_tests):
            self.object_state_list.remove(bad)


    def equal_call_traces(self, lhs, rhs):
        """ Returns if the traces are the same """

        dict_keys_to_compare = ['type', 'func', 'return', 'inputs', 'vals']

        # Basic check on lengths of stacks
        if len(lhs) != len(rhs):
            return False

        # Look through stacks, filter to values interested in and then compare
        for x in xrange(len(lhs)):

            lhs_filtered = filter(lambda (k, v): k in dict_keys_to_compare, lhs[x].items())
            rhs_filtered = filter(lambda (k, v): k in dict_keys_to_compare, rhs[x].items())

            if lhs_filtered != rhs_filtered:
                return False

        return True


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



