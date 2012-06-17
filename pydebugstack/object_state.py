
class ObjectState():
    """ Class to hold the state of an object """

    def __init__(self, class_name):
        """ Init """ 

        self.call_trace = [] # The trace of calls in the class of interest
        self.last_val_obj = None # Stores a copy of the attributes of the object when we last were executing a method 
        self.call_stack = [] # Current call stack in the object of iterest
        self.class_name = class_name # Name of class being watched - TODO assert this is correct on calls

    def function_call(self, local_vars, func_name):
        """ A call to a function """

        # Save the current call stack just within the object
        self.call_stack.append(func_name)

        # Detect if there have been changes to the attributes between the call
        new_val_obj = self.create_obj_attr_dict(local_vars['self'])
        if (self.last_val_obj != None) and (self.last_val_obj != new_val_obj):
            self.call_trace.append({
                'type': 'attr_change',
                'vals': self.changes_between_dict(self.last_val_obj, new_val_obj),
            })

    def function_return(self, local_vars, func_name):
        """ A return from a function """

        # Take this func now off the stack
        return_func = self.call_stack.pop()
        assert (return_func == func_name)

        # If we have a call stack then this was a call originiating inside the object so ignore it
        if len(self.call_stack) == 0:
        
            # Get the actual params passed in
            inputs = local_vars.copy()
            del inputs['self']
            del inputs['__return__']

            self.call_trace.append({
                'type': 'func_call',
                'func': func_name, 
                'return': local_vars['__return__'],
                'inputs': inputs,
            })

        # Save current state of object attributes
        self.last_val_obj = self.create_obj_attr_dict(local_vars['self'])


    def var_constructor(self, var_in, new_var_name):
        """ Returns a list of code that would reconstruct the given object """

        if type(var_in) in [bool, int, list, set, dict]:
            return [
                "{} = {}".format(new_var_name, var_in),
                "assert(ret == expected_return)"
            ]
        else:
            output_list = []
            
            output_list.append("{} = {}.{}()".format(new_var_name, var_in.__class__.__module__, var_in.__class__.__name__))
            output_list = output_list + [ "setattr({}, '{}', {})".format(new_var_name, k, var_in.__dict__[k]) for k in var_in.__dict__.keys() ]

            # TODO attempt to eval this and if fails go to pickle??

            output_list.append("assert(ret.__dict__ == expected_return.__dict__)")
            return output_list 


    def format_input_text(self, inputs):
        
        return ", ".join([ "{}={}".format(k, v) for (k, v) in inputs.items() ])

    def output_test_code(self):

        code_out = []

        code_out.append("""print "Starting execution of autogen test harness for {}" """.format(self.class_name))
        code_out.append("")

        # Create obj if we have no explict __init__call
        if len(filter(lambda x: x['type'] == 'func_call' and x['func'] == "__init__", self.call_trace)) == 0:
            code_out.append("# Object initialiser - no actual function")
            code_out.append("obj_var = {}()".format(self.class_name))
            code_out.append("")

        # We must have a call trace to do this
        assert len(self.call_trace) > 0

        # Handle all trace items
        for call in self.call_trace:

            # Change in attribute types
            if call['type'] == "attr_change":
                    code_out.append("# Attributes changed directly")
                    for k, v in call['vals'].items():                    
                        code_out.append("obj_var.{} = {}".format(k,v))

            # Function                         
            else:

                # Init
                if call['func'] == "__init__":
                    code_out.append("# Object initialiser with params")
                    code_out.append("obj_var = {}({})".format(self.class_name, self.format_input_text(call['inputs'])))
                # Func with return
                elif call['return'] != None:
                    code_out.append("# Call to {} with return".format(call['func']))
                    code_out.append("ret = obj_var.{}({})".format(call['func'], self.format_input_text(call['inputs'])))
                    code_out = code_out + self.var_constructor(call['return'], "expected_return")
                # Func no return
                else:
                    code_out.append("# Call to {}".format(call['func']))
                    code_out.append("obj_var.{}({})".format(call['func'], self.format_input_text(call['inputs'])))
                
            code_out.append("")
       
        code_out.append("""print "Done with execution of autogen test harness for {}" """.format(self.class_name))
        code_out.append("") 

        return "\n".join(code_out)


    def create_obj_attr_dict(self, obj):
        """ Creates a dictionary with just the object attributes """

        # TODO this should just be a utility

        attr_out = {}
       
        import types

        for attr_name in dir(obj):
            if not attr_name.startswith('__'):
                attr_val = getattr(obj, attr_name) 
                if not type(attr_val) is types.MethodType:
                    attr_out[attr_name] = attr_val

        return attr_out


    def changes_between_dict(self, old, new):
        """ finds the differences in the dicts and returns the changes requried to old to get to new """

        # TODO utility 

        changes_to_new = {}

        for key in new.keys():
            if key in old:
                if old[key] != new[key]:
                    changes_to_new[key] = new[key]
            else:
                changes_to_new[key] = new[key]
        
        return changes_to_new

