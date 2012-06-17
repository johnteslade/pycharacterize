import logging

class ObjectCodeOutput():
    """ Class to handle the outputting of code for the object """

    def output_test_code(self, object_state):
        """ Returns the code for the test harness """

        logging.info("Stack out = {}".format(object_state.call_trace))

        code_out = []

        code_out.append("""print "Starting execution of autogen test harness for {}" """.format(object_state.class_name))
        code_out.append("")
        code_out.append("from object_factory import object_factory")
        code_out.append("")

        # Create obj if we have no explict __init__call
        if len(filter(lambda x: x['type'] == 'func_call' and x['func'] == "__init__", object_state.call_trace)) == 0:
            code_out.append("# Object initialiser - no actual function")
            code_out.append("obj_var = {}()".format(object_state.class_name))
            code_out.append("")

        # We must have a call trace to do this
        assert len(object_state.call_trace) > 0

        # Handle all trace items
        for call in object_state.call_trace:

            # Change in attribute types
            if call['type'] == "attr_change":
                    code_out.append("# Attributes changed directly")
                    for k, v in call['vals'].items():                    
                        code_out.append("obj_var.{} = {}".format(k,v))

            # Function                         
            else:

                # Init
                if call['func'] == "__init__":
                    code_out.append("# Object initialiser")
                    code_out.append("obj_var = {}({})".format(object_state.class_name, self.format_input_text(call['inputs'])))

                # Function call
                else:
                    code_out.append("# Call to {}".format(call['func']))
               
                    func_inputs = self.format_input_text(call['inputs']) 

                    if call['return'] != None:
                        code_out.append("ret = obj_var.{}({})".format(call['func'], func_inputs))
                        code_out.append("expected_return = {}".format(self.print_var(call['return'])))
                        
                        # Determine best method for comparison
                        # TODO more complex types will need different comparison types
                        if hasattr(call['return'], "__dict__"):                        
                            code_out.append("assert(ret.__dict__ == expected_return.__dict__)")
                        else:
                            code_out.append("assert(ret == expected_return)")

                    else:
                        code_out.append("obj_var.{}({})".format(call['func'], func_inputs))
                
            code_out.append("")
       
        code_out.append("""print "Done with execution of autogen test harness for {}" """.format(object_state.class_name))
        code_out.append("") 

        return "\n".join(code_out)


    def format_input_text(self, inputs):
        """ Formats function parameter types """

        return ", ".join([ "{}={}".format(k, self.print_var(v)) for (k, v) in inputs.items() ])


    def print_var(self, var_in):
        """ Function returns string representation of object so it can be reconstructed """
        
        # Basic type
        if (var_in == None) or (type(var_in) in [bool, int, str]):
            return "{}".format(var_in)
        # List
        elif type(var_in) == list:
            converted_items = [ self.print_var(x) for x in var_in ]
            return "[" + ", ".join(converted_items) + "]"
        # Dictionary
        elif type(var_in) == dict:
            converted_items = [ "'{}': {}".format(k, self.print_var(v)) for k, v in var_in.items() ]
            return "{" + ", ".join(converted_items) + "}"
        # Tuples
        elif type(var_in) == tuple:
            converted_items = [ self.print_var(x) for x in var_in ]
            return "(" + ", ".join(converted_items) + ")"
        # Object - TODO not sure if this the best way to determine it
        elif hasattr(var_in, "__dict__"):
            return "object_factory({}.{}, {})".format(var_in.__class__.__module__, var_in.__class__.__name__, self.print_var(var_in.__dict__))
        # An unknown variable
        else:
            return "None"

if __name__ == "__main__":
    
    from object_factory import object_factory
    import mytest
    
    def test_print_var_cycle(var_in):

        print "Var in: {}".format(var_in)
        
        printed_var = output_o.print_var(var_in)
        print "Printed var: {}".format(printed_var)

        eval_printed_var = eval(printed_var)
        print "Eval printed var: {}".format(eval_printed_var)

        if ( hasattr(var_in, "__dict__") and (eval_printed_var.__dict__ == var_in.__dict__) ) or (eval_printed_var == var_in):
            print "SAME vars"
        else:
            print "ERROR: not reproducable"

        print "----------"


    output_o = ObjectCodeOutput()

    test_print_var_cycle(1)
    
    test_print_var_cycle([1, 2, 3])
    
    test_print_var_cycle((1, 2, 3))
    
    test_print_var_cycle({'a': 1, 'b': 2, 'c': 3})
    
    test_print_var_cycle({'a': (1, 2), 'b': [3, 4], 'c': 3})
    
    test_print_var_cycle(mytest.AnObject())

    test_print_var_cycle([mytest.AnObject(x=1), mytest.AnObject(x=2), mytest.AnObject(x=3)])


