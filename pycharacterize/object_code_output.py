import logging
import re
import jsonpickle

class ObjectCodeOutput():
    """ Class to handle the outputting of code for the object """

    INDENT_SIZE = 4 # Number of spaces to indent
    INDENT_STRING = (" " * INDENT_SIZE) # A string for one indent

    def output_test_code(self, object_state_list, **kwarg):
        """ Returns the code for the test harness """
        
        return "\n".join(self.output_test_code_list(object_state_list, **kwarg))


    def output_test_code_annotated(self, object_state):
        """ Returns the code for the test harness with annotations """
        
        code_lines = self.output_test_code_list(object_state_list)

        for i in xrange(len(code_lines)):
            code_lines[i] = ("%03d:" % i) + code_lines[i]

        return "\n".join(code_lines)

    def output_test_code_list(self, object_state_list, **kwarg):

        logging.info("State list = {}".format(object_state_list))
        logging.info("State list len = {}".format(len(object_state_list)))

        code_out = []
        
        test_case_name = "Test_{}".format(object_state_list[0].class_name.replace(".", "_"))

        # Define the initial code
        code_out.append("import unittest")
        code_out.append("import {}".format(object_state_list[0].class_name.split(".")[0]))
        code_out.append("") 
        code_out.append("class {}(unittest.TestCase):".format(test_case_name))
        code_out.append(self.INDENT_STRING) 
        
        for x in xrange(len(object_state_list)):
            code_out.append(self.INDENT_STRING + "def test_MyTest_{}(self):".format(x + 1))
            code_out.append(self.INDENT_STRING) 
            code_out = code_out + [ self.INDENT_STRING + self.INDENT_STRING + line for line in self.output_test_code_single_test(object_state_list[x], x, **kwarg) ]

        # Code at end of code
        code_out.append("suite = unittest.TestLoader().loadTestsFromTestCase({})".format(test_case_name))
        code_out.append("unittest.TextTestRunner(verbosity=2).run(suite)")

        return code_out


    def output_test_code_single_test(self, object_state, test_num, **kwarg):
        """ Returns the code as a single test """

        logging.info("Stack out = {}".format(object_state.call_trace))

        logging.debug("Call stack = {}".format(object_state.call_trace))


        code_out = []
        
        code_out.append("""print "Starting execution of autogen test harness for {}" """.format(object_state.class_name))
        code_out.append("")
        code_out.append("from pycharacterize.object_factory import object_factory")
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
              
                    if 'backtrace' in kwarg and kwarg['backtrace'] == True:
                        for stack in call['stack'][1:-1]: 
                            code_out.append("# Backtrace: {}".format(stack))
              

                    func_inputs = self.format_input_text(call['inputs']) 

                    if call['return'] != None:
                        code_out.append("ret = obj_var.{}({})".format(call['func'], func_inputs))
                        code_out.append("expected_return = {}".format(self.print_var(call['return'])))
                        
                        # Determine best method for comparison
                        # TODO more complex types will need different comparison types
                        if hasattr(call['return'], "__dict__"):                        
                            code_out.append("self.assertEqual(ret.__dict__, expected_return.__dict__)")
                        else:
                            code_out.append("self.assertEqual(ret, expected_return)")

                    else:
                        code_out.append("obj_var.{}({})".format(call['func'], func_inputs))
                
            code_out.append("")
       
        code_out.append("""print "Done with execution of autogen test harness for {}" """.format(object_state.class_name))
        code_out.append("") 

        return code_out


    def format_input_text(self, inputs):
        """ Formats function parameter types """

        return ", ".join([ "{}={}".format(k, self.print_var(v)) for (k, v) in inputs.items() ])


    def print_var(self, var_in, depth=1):
        """ Function returns string representation of object so it can be reconstructed """
       
        print "depth = {}".format(depth)

        if depth > 10:
            print "Too deep"
            return "None"

        # Basic type
        if (var_in == None) or (type(var_in) in [bool, int]):
            return "{}".format(var_in)
        # String (special behaviour to escape)
        elif type(var_in) == str:
            return "'{}'".format(var_in)
        # Is this a type
        elif type(var_in) == type:
            class_match = re.match("^<class '(.*)'>$", str(var_in))
            if class_match: 
                return class_match.group(1)
            else:
                print "Unknown type - {}".format(type(var_in))
                return "UNKNOWN_TYPE({} {})".format(var_in, type(var_in))

        # List
        elif type(var_in) == list:
            converted_items = [ self.print_var(x, depth + 1) for x in var_in ]
            return "[" + ", ".join(converted_items) + "]"
        # Dictionary
        elif type(var_in) == dict:
            converted_items = [ "'{}': {}".format(k, self.print_var(v, depth + 1)) for k, v in var_in.items() ]
            return "{" + ", ".join(converted_items) + "}"
        # Tuples
        elif type(var_in) == tuple:
            converted_items = [ self.print_var(x, depth + 1) for x in var_in ]
            return "(" + ", ".join(converted_items) + ")"
        # Object - TODO not sure if this the best way to determine it
        elif hasattr(var_in, "__dict__"):
            return self.create_object_factory_call(var_in)
        # An unknown variable
        else:
            return "None"

    def create_object_factory_call(self, var_in):
        """ Returns the string needed for an object_factory call """
       
        # Pickle the object - set the options to intent lines
        p = jsonpickle.JSONPluginMgr() 
        p.set_encoder_options('simplejson', sort_keys=True, indent=self.INDENT_SIZE)
        j = jsonpickle.pickler.Pickler()
        encoded_obj = p.encode(j.flatten(var_in))
        
        encoded_obj = encoded_obj.replace("'", "\\'")
        encoded_obj = encoded_obj.replace('\\"', '\\\\"')
        
        return "object_factory(\"\"\"{}\"\"\")".format(encoded_obj)



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


