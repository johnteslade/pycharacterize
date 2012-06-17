
class ObjectCodeOutput():
    """ Class to handle the outputting of code for the object """

    def output_test_code(self, object_state):

        code_out = []

        code_out.append("""print "Starting execution of autogen test harness for {}" """.format(object_state.class_name))
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
                    code_out.append("# Object initialiser with params")
                    (func_inputs, additional_constructors) = self.format_input_text(call['inputs']) 
                    code_out += additional_constructors
                    code_out.append("obj_var = {}({})".format(object_state.class_name, func_inputs))

                # Function call
                else:
                    code_out.append("# Call to {}".format(call['func']))
               
                    (func_inputs, additional_constructors) = self.format_input_text(call['inputs']) 
                    code_out += additional_constructors

                    if call['return'] != None:
                        code_out.append("ret = obj_var.{}({})".format(call['func'], func_inputs))
                        code_out = code_out + self.var_constructor(call['return'], "expected_return", True)
                    else:
                        code_out.append("obj_var.{}({})".format(call['func'], func_inputs))
                
            code_out.append("")
       
        code_out.append("""print "Done with execution of autogen test harness for {}" """.format(object_state.class_name))
        code_out.append("") 

        return "\n".join(code_out)


    def var_constructor(self, var_in, new_var_name, with_assert):
        """ Returns a list of code that would reconstruct the given object """

        output_list = []

        if self.can_print_var(var_in):
            output_list.append("{} = {}".format(new_var_name, var_in))
            if with_assert:
                output_list.append("assert(ret == {})".format(new_var_name))
        
        else:
            
            output_list.append("{} = {}.{}()".format(new_var_name, var_in.__class__.__module__, var_in.__class__.__name__))
            output_list = output_list + [ "setattr({}, '{}', {})".format(new_var_name, k, var_in.__dict__[k]) for k in var_in.__dict__.keys() ]

            # TODO attempt to eval this and if fails go to pickle??

            if with_assert:
                output_list.append("assert(ret.__dict__ == {}.__dict__)".format(new_var_name))
        
        return output_list 


    def format_input_text(self, inputs):
       
        input_list = []
        additional_constructors = []

        var_int = 0

        for (k, v) in inputs.items(): 
            if self.can_print_var(v):
                input_list.append("{}={}".format(k, v))
            else:
                var_int += 1
                temp_obj_name = "temp_var_{}".format(var_int)

                additional_constructors += self.var_constructor(v, temp_obj_name, False)

                input_list.append("{}={}".format(k, temp_obj_name))
        
        return (", ".join(input_list), additional_constructors)


    def can_print_var(self, var_in):
        """ Can the variable be printed and then reconstructed? """
        
        return type(var_in) in [bool, int, list, set, dict]



