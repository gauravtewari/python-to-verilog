#!/usr/bin/python3

from optparse import OptionParser
import configparser
from ver import verCode
from ver import num_bits

def main():
    parser = OptionParser("usage: %ver -s filename -m modulename", version="py2ver 1.0")

    parser.add_option("-s","--desc_file", dest="sm_file", help="Enter the state machine description file")
    parser.add_option("-m", "--module", dest="module_name", help="Enter the name of the verilog module")
    
    (options,args) = parser.parse_args()
    

    #if len(sys.argv) != 3:
    #    print("Usage: ver.py [module_name] [state_machine config file]")
    #    sys.exit(1)
    if (options.sm_file is None or options.module_name is None):
        parser.error("Enter the filename and module name");

    #Create a class
    
    obj = verCode(options.sm_file, options.module_name)
    obj.print_source()


if __name__ == "__main__":
    main()

class write_source:
    def gen_source(self, sm_file, module):
        code = verCode(sm_file, module)
        print("Source file : {} \nTestbench : {} \nSM : {}".format(code.source_file(), code.tb_file(), code.conf_file()))
