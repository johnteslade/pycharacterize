PyCharacterize
==============

PyCharacterize is a library to help autogenerate test cases for existing Python code to capture their current behaviour.  This is useful when attempting to refactor code which has little or no test coverage.

More detail on characterization tests can be found on Wikipedia http://en.wikipedia.org/wiki/Characterization_test

Why did I create this
---------------------

In my software development experience I have come across many situations where parts of the source code need refactoring or improving but are missing even basic test harnesses.  Refactoring without test harnesses is dangerous as it's very easy to introduce bugs and then have to spend a long time debugging.  I'm of the opinion that refactoring needs a very quick - make some small changes, run tests to ensure nothing is broken, repeat....

I chose to do this for Python because of its ability to easily access the internal state of objects and I also wanted to learn more about Python and its internals.

Example
-------

The following example uses a test on yum (the Fedora package manager).

The code in this example is simplified but the full source code is in the repository https://github.com/johnteslade/pycharacterize/blob/master/example/yum/

The class of interest (i.e. the one we want test cases for) was choosen as yum.config.BoolOption - the source of this is http://yum.baseurl.org/gitweb?p=yum.git;a=blob;f=yum/config.py;h=5856aa27d3d763c28b7745b1cfc8b8b7f28523e0;hb=HEAD#l378

The way to invoke the entire program is by calling yummain.user_main() - this will then start the program and somewhere this through a complex nest of functions will eventually use yum.config.BoolOption

The way to use pycharacterize to generate the tests is as follows:

    # Setup to create tests for the yum.config.BoolOption class
    pdb_obj = pycharacterize.runner.Runner()
    pdb_obj.set_class_to_watch(yum.config.BoolOption, "yum.config.BoolOption")

    # Execute yum
    pdb_obj.do_runcall(yummain.user_main, [], exit_code=True)

    # Output the generated tests
    pdb_obj.output_test_code_to_file("testcases_yum.py")

This will run the program and generate us pyunit tests:

    class Test_yum_config_BoolOption(unittest.TestCase):
        
        def test_MyTest_1(self):
        
            obj_var = yum.config.BoolOption(default=False, parse_default=False)
            
            # Call to parse
            ret = obj_var.parse(s='0')
            expected_return = False
            self.assertEqual(ret, expected_return)
            
        def test_MyTest_2(self):
        
            # Object initialiser
            obj_var = yum.config.BoolOption(default=False, parse_default=False)
            
            # Call to parse
            ret = obj_var.parse(s='1')
            expected_return = True
            self.assertEqual(ret, expected_return)


Limitations
-----------

The more complex parameters that get used (e.g. nested objects) the more likely something will go wrong with the test code generation.

Objects that use __slots__ (http://docs.python.org/2/reference/datamodel.html#slots) also cannot easily be serialised so this is likely to break.

However, dispite these limitations pycharacterize is designed to give you a starting point for test coverage.  If you know how the program works it is likely you can hand modify the tests for better results.

How it works
------------

Pycharacterize is based on the python debugger pdb.  This is used to step through the source code and detect when the class we are watching is created and called.  The calling parameters, attributes and return values are then captured and used to generate the test cases.

