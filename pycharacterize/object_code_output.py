import logging
import re
import jsonpickle

from jinja2 import Environment, PackageLoader

class ObjectCodeOutput():

    """ Class to handle the outputting of code for the object """

    INDENT_SIZE = 4 # Number of spaces to indent

    def output_test_code(self, object_state_list, **kwarg):
        """ Returns the code for the test harness """
        
        return self.output_test_code_list(object_state_list, **kwarg)


    def output_test_code_annotated(self, object_state):
        """ Returns the code for the test harness with annotations """
        
        code_lines = self.output_test_code_list(object_state_list)

        for i in xrange(len(code_lines)):
            code_lines[i] = ("%03d:" % i) + code_lines[i]

        return "\n".join(code_lines)

    def output_test_code_list(self, object_state_list, **kwarg):

        logging.info("State list = {}".format(object_state_list))
        logging.info("State list len = {}".format(len(object_state_list)))

        # Get jinja environment and templates
        env = Environment(loader=PackageLoader('pycharacterize', 'templates'), trim_blocks=True, lstrip_blocks=True)
        env.filters['format_input_text'] = self.format_input_text 
         
        template = env.get_template('testcase.tpl.py') 

        test_case_name = "Test_{}".format(object_state_list[0].class_name.replace(".", "_"))
       
        test_cases = []

        for x in xrange(len(object_state_list)):
            
            test_cases.append(self.output_test_code_single_test(object_state_list[x], x, **kwarg))

        return template.render({
            'module': object_state_list[0].class_name.split(".")[0], 
            'class_name': object_state_list[0].class_name,
            'class_name_var': object_state_list[0].class_name.replace(".", "_"),
            'test_cases': test_cases,
            'backtrace': ('backtrace' in kwarg and kwarg['backtrace'] == True),
        })


    def output_test_code_single_test(self, object_state, test_num, **kwarg):
        """ Returns the code as a single test """

        logging.info("Stack out = {}".format(object_state.call_trace))

        logging.debug("Call stack = {}".format(object_state.call_trace))

        assert len(object_state.call_trace) > 0

        return {
            'no_init': (len(filter(lambda x: x['type'] == 'func_call' and x['func'] == "__init__", object_state.call_trace)) == 0),
            'call_trace': object_state.call_trace,
             
        }

    
    def format_input_text(self, inputs):
        """ Formats function parameter types """

        if type(inputs) == dict:
            return ", ".join([ "{}={}".format(k, self.print_var(v)) for (k, v) in inputs.items() ])
        else:
            return self.print_var(inputs)


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
            type_details = self.get_type_class(var_in)
            if type_details: 
                return type_details
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

        # Detect slots objects
        if hasattr(var_in, "__slots__"): 

            # Try and use repr to recreate  
            repr_result = self.repr_encode(var_in)

            if repr_result:
                return repr_result
            else:
                # TODO should this be fatal?
                logging.warning("Cannot pickle as object uses __slots__")
                logging.warning("repr result = {}".format(self.repr_encode(var_in)))
                return "None"

        else:
            # Pickle the object - set the options to intent lines
            p = jsonpickle.JSONPluginMgr() 
            p.set_encoder_options('simplejson', sort_keys=True, indent=self.INDENT_SIZE)
            j = jsonpickle.pickler.Pickler()
            encoded_obj = p.encode(j.flatten(var_in))
            
            encoded_obj = encoded_obj.replace("'", "\\'")
            encoded_obj = encoded_obj.replace('\\"', '\\\\"')
            
            return "object_factory(\"\"\"{}\"\"\")".format(encoded_obj)


    def repr_encode(self, var_in):
        """ Attempts to use repr to reconstruct object """

        repr_result = repr(var_in)

        class_type = self.get_type_class(var_in.__class__)
        module_name = ".".join(class_type.split(".")[:-1])

        logging.debug("repr = {} type = {} module = {}".format(repr_result, class_type, module_name))

        repr_result = module_name + "." + repr_result

        code_ok = True

        try:
            __import__(module_name)
        except Exception as e:
            code_ok = False
            logging.warning("import of {} failed = {}".format(module_name, e))

        try:
            test_obj = eval(repr_result)
        except Exception as e:
            code_ok = False
            logging.warning("eval of |{}| failed = {}".format(repr_result, e))

        if code_ok:
            return repr_result
        else:
            return None
        
        
    def get_type_class(self, var_in):
        """ Returns a string of the type info """

        # TODO there must be a better way of doing this - given that the interactive python shell can print it directly

        class_match = re.match("^<class '(.*)'>$", str(var_in))
        if class_match: 
            return class_match.group(1)
        else:
            return None



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


