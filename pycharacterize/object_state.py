import types
import logging


class ObjectState(object):
    """ Class to hold the state of an object """

    def __init__(self, class_name, id_in):
        """ Init """

        self.call_trace = [] # The trace of calls in the class of interest
        self.last_val_obj = None # Stores a copy of the attributes of the object when we last were executing a method
        self.call_stack = [] # Current call stack in the object of iterest
        self.class_name = class_name # Name of class being watched - TODO assert this is correct on calls
        self.id = id_in # The id of this object being represented


    def function_call(self, local_vars, func_name):
        """ A call to a function """

        # Save the current call stack just within the object
        self.call_stack.append(func_name)

        logging.debug("function_call: stack = {}".format(self.call_stack))

        # Only check for differences if we one level into object
        if len(self.call_stack) == 1:
            # Detect if there have been changes to the attributes between the call
            new_val_obj = self.create_obj_attr_dict(local_vars['self'])
            if (self.last_val_obj != None) and (self.last_val_obj != new_val_obj):
                self.call_trace.append({
                    'type': 'attr_change',
                    'vals': self.changes_between_dict(self.last_val_obj, new_val_obj),
                })

        # Save current state of object attributes
        self.last_val_obj = self.create_obj_attr_dict(local_vars['self'])

        # Save current state of object attributes
        self.last_val_obj = self.create_obj_attr_dict(local_vars['self'])

    def function_return(self, local_vars, func_name, stack):
        """ A return from a function """

        # Take this func now off the stack
        return_func = self.call_stack.pop()

        logging.debug("function_return: stack = {}".format(self.call_stack))

        if (return_func != func_name):
            logging.warn("Error with call stack return_func = {}, func_name = {}, call_stack = {}".format(return_func, func_name, self.call_stack))

        assert (return_func == func_name)

        # If we have a call stack then this was a call originiating inside the object so ignore it
        if len(self.call_stack) == 0 and func_name not in ['__get__', '__set__']:

            # Get the actual params passed in
            inputs = local_vars.copy()
            del inputs['self']
            del inputs['__return__']
            if '__exception__' in inputs:
                del inputs['__exception__']

            back_trace = []

            for (frame, lineno) in stack:
                back_trace.append("{}() at {}:{}".format(frame.f_code.co_name, frame.f_code.co_filename, lineno))

            call_details = {
                'type': 'func_call',
                'func': func_name,
                'return': local_vars['__return__'],
                'inputs': inputs,
                'stack': back_trace,
            }

            if '__exception__' in local_vars:
                call_details['exception'] = local_vars['__exception__'][0]

            self.call_trace.append(call_details)

        # Save current state of object attributes
        self.last_val_obj = self.create_obj_attr_dict(local_vars['self'])


    def create_obj_attr_dict(self, obj):
        """ Creates a dictionary with just the object attributes """

        attr_out = {}

        for attr_name in dir(obj):
            if not attr_name.startswith('__'):
                attr_val = getattr(obj, attr_name)
                if not type(attr_val) is types.MethodType:
                    attr_out[attr_name] = attr_val

        return attr_out


    def changes_between_dict(self, old, new):
        """ finds the differences in the dicts and returns the changes requried to old to get to new """

        changes_to_new = {}

        for key in new.keys():
            if key in old:
                if old[key] != new[key]:
                    changes_to_new[key] = new[key]
            else:
                changes_to_new[key] = new[key]

        return changes_to_new

