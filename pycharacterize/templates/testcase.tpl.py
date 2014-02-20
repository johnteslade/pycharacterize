
import unittest
import {{ module }}

class Test_{{ class_name_var }}(unittest.TestCase):
{% for test in test_cases %}
    def test_MyTest_{{ loop.index }}(self): 

        print "Starting execution of autogen test harness for {{ class_name }}" 
        
        from pycharacterize.object_factory import object_factory

        {# Create obj if we have no explict __init__ call #}    
        {% if test.no_init %}
        # Object initialiser - no actual function
        obj_var = {{ class_name }}()
        {% endif %}

        {# Look at all the call traces #}
        {% for call in test.call_trace %}
        
        {% if call.type == "attr_change" %}
        # Attributes changed directly
        {% for key, value in call.vals.iteritems() %}
        obj_var.{{ key }} = {{ value }}
        {% endfor %}
        {% elif call.type == "func_call" %}

        {% if call.func == "__init__" %}

        # Object initialiser
        obj_var = {{ class_name }}({{ call.inputs|format_input_text }})

        {% else %}

        # Call to {{ call.func }}
        {% if backtrace %}
        {% for stack in call.stack[1:-1] %}
        # Backtrace: {{ stack }}
        {% endfor %}
        {% endif %}
        
        {% if call.return != None %}

        ret = obj_var.{{ call.func }}({{ call.inputs|format_input_text }})
        expected_return = {{ call.return|format_input_text }}
        {% if call.return_dict %}
        self.assertEqual(ret.__dict__, expected_return.__dict__)
        {% else %}
        self.assertEqual(ret, expected_return)
        {% endif %}

        {% else %}
        obj_var.{{ call.func }}({{ call.inputs|format_input_text }})
        {% endif %}
        {% endif %}
        {% endif %}
        {% endfor %}
        print "Done with execution of autogen test harness for {{ class_name }}"

{% endfor %}
suite = unittest.TestLoader().loadTestsFromTestCase(Test_{{ class_name_var }})
unittest.TextTestRunner(verbosity=2).run(suite)

