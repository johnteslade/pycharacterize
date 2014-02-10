
import unittest
import {{ module }}

class {{ test_case_name }}(unittest.TestCase):

{{ test_cases }}

suite = unittest.TestLoader().loadTestsFromTestCase({{ test_case_name }})
unittest.TextTestRunner(verbosity=2).run(suite)

