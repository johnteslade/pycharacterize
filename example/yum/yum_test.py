# Modify paths so import pycharacterize works
import sys
sys.path.append("../../")
sys.path.append("../")
sys.path.append(".")

# Import the pycharacterise lib
import pycharacterize 

# Import the yum classes
sys.path.insert(0, '/usr/share/yum-cli')
import yummain
import yum

# Setup to create tests for the yum.config.BoolOption class
pych_obj = pycharacterize.runner.Runner()
pych_obj.set_class_to_watch(yum.config.BoolOption, "yum.config.BoolOption")

# Execute yum
pych_obj.do_runcall(yummain.user_main, [], exit_code=True)

# Output the generated tests
pych_obj.output_test_code_to_file("testcases_yum.py")

        
