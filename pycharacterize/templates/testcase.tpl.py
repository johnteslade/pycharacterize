
import unittest
import {{ module }}

class {{ test_case_name }}(unittest.TestCase):

{% for test in test_cases %}

    def test_MyTest_{{ loop.index }}(self): 
        {% for test_line in test %}{{ test_line }}
        {% endfor %}

{% endfor %}

suite = unittest.TestLoader().loadTestsFromTestCase({{ test_case_name }})
unittest.TextTestRunner(verbosity=2).run(suite)

