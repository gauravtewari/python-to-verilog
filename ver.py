

import sys

import configparser

def num_bits(num):
    n = int(num)
    nbits = 0
    while n > 0:
        n = int(n/2)
        nbits = nbits+1
    return nbits


'''
Generates the Verilog Source code for given state machine
'''
class verCode:
    def __init__(self, sm, name='source'):
        self.source = name
        self.conf = sm
        self.in_ports = ['clock', 'reset_n', 'in', 'x']
        self.out_ports = ['out']
        self.params = []
        self.states = {}
        self.transitions = {}
        self.numbits = 0
        try:
            self.src_out = open(self.source+".v", 'w')
        except IOError:
            print("Error opening file")
            sys.exit(1)
        self.parse_sm()

    def source_file(self):
        return self.source+".v"

    def conf_file(self):
        return self.conf

    # parse sections from state machine configuration file
	# For a given section in a config file, returns the key value pairs as a python dict
    def config_sec(self, section):
        dict1 = {}
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option]=self.config.get(section, option)
                if dict1[option] == -1:
                    print("skip : %s"%option);
            except:
                print("Exception on %s!"%option)
                dict1[option] = None
        return dict1

    # parse the state machine configuration file
    # Extracts the Moore type state machine parameters from given configuration file
    def parse_sm(self):
		
		# Initialize the parser
        self.config = configparser.ConfigParser()
		# Read the configuration file
        self.config.read(self.conf)
        # Check if states are present in configuration file
        if 'states' not in self.config.sections():
            print("Error parsing config file: States not found");
            sys.exit(1);
        # Check if transitions are present in configuration file
        if 'transitions' not in self.config.sections():
            print("Error transitions not found in config file")
            sys.exit(0);
        # Check if IDLE state configuration is present
        if 'idle' not in self.config.sections():
            print("Error no idle state transitions found in config file")
            sys.exit(0);
	
        # Get the states from configuration file
        self.states = self.config_sec('states');
        
        # Get the transitions for each states
        self.transitions = self.config_sec('transitions');
        
        # Get the IDLE state information and do sanitory checks
        self.idle = self.config_sec('idle');
        if self.idle['next'] not in self.states.keys():
            print("Next state for idle is not in given state values")
            sys.exit(1)
        
        # Check whether there is transition for each state.
        # Transitions dict contains transition values for each state key.
        # Split the transitions as separte items of a list
        for key in self.states.keys():
            if key not in self.transitions.keys():
                print("Transition not found for {}".format(key))
                sys.exit(1)
            # for a list of transitions
            self.transitions[key] = self.transitions[key].split();
		
		# Number of bits required to store the states
        self.numbits = num_bits(len(self.states.keys())+1)
        
    # Print the if construct.
    def print_if(self, in_val, x_val, next_state, level, f=sys.stdout):
        for i in range(level):
            print("\t", end='', file=f)
        if in_val == 'x':
            print("if( x == 1'b{})".format(x_val), file=f)
        elif x_val == 'x':
            print("if( in == 1'b{})".format(in_val), file=f)
        else:
            print("if( in == 1'b{} && x == 1'b{})".format(in_val, x_val), file=f)
        for i in range(level):
            print("\t", end='', file=f)
        print("\tstate = {};".format(next_state), file=f)
        
    # Print the else if construct in verilog
    def print_elif(self, in_val, x_val, next_state, level, f=sys.stdout):
        for i in range(level):
            print("\t", end='', file=f )
        if in_val == 'x':
            print("else if( x == 1'b{})".format(x_val), file=f )
        elif x_val == 'x':
            print("else if( in == 1'b{})".format(in_val), file=f )
        else:
            print("else if( in == 1'b{} && x == 1'b{})".format(in_val, x_val), file=f )
        for i in range(level):
            print("\t", end='', file=f )
        print("\tstate = {};".format(next_state), file=f )
    
    # Print the else construct in verilog
    def print_else(self, next_state, level, f=sys.stdout):
        for i in range(level):
            print("\t", end='', file=f )
        print("else", file=f )
        for i in range(level):
            print("\t", end='', file=f )
        print("\tstate = {};".format(next_state), file=f )

	# Print the state transition code in verilog source file
    def print_state(self, level, f=sys.stdout):
        for i in range(level):
            print("\t", end='', file=f)
        print("idle:", file=f)
        for i in range(level):
            print("\t", end='', file=f)
        print("\tstate = {};".format(self.idle['next']), file=f)
        for key in (sorted(self.states.keys())):
            for i in range(level):
                print("\t", end='', file=f )
            print("{}:".format(key), file=f )
            num = len(self.transitions[key])
            if num == 0 or num > 4:
                print("Wrong transition values for state {}".format(key))
                sys.exit(0)
            for i, t in enumerate(self.transitions[key]):
                tr = t.split(':',1) # list containing 'ab', 'next_state'
                next_state = tr[1];
                in_val = tr[0][0]
                x_val = tr[0][1]
                if i == 0:
                    self.print_if(in_val, x_val, next_state, level+1, f)
                elif i == 3:
                    continue
                else:
                    self.print_elif(in_val, x_val, next_state, level+1, f)
            self.print_else(key, level+1, f)
    
    # Print the next state always block in verilog source file
    def next_state_logic(self):
        print("\n/* Next state logic */", file=self.src_out)
        print("always @(posedge {} or negedge {}) begin".format(self.in_ports[0], self.in_ports[1]), file = self.src_out)
        print("\tif (!{})\n\t\tstate = idle;\n\telse".format(self.in_ports[1]), file=self.src_out);
        print("\t\tcase(state)", file=self.src_out)
        self.print_state(3, self.src_out)
        print("\t\tendcase",file=self.src_out)
        print("end",file=self.src_out)
    
    # Print the state parameter declaration
    def print_state_params(self):
        print("\nreg [{}:0] state;".format(self.numbits-1), file=self.src_out)
        print("parameter\tidle = 0,", file=self.src_out)
        count = 1
        l = sorted(self.states.keys())
        for i in range(len(l)-1):
            print("\t\t{0} = {1:d},".format(l[i], count), file = self.src_out)
            count = count+1
        print("\t\t{0} = {1:d};".format(l[-1], count), file=self.src_out)
    
    # Print the output always construct for state machine in verilog source file
    def out_logic(self, level, f=sys.stdout):
        l = sorted(self.states.keys())
        for i in l:
            for tab in range(level):
                print("\t", end='', file=f)
            print("{}:".format(i), file=f)
            for tab in range(level):
                print("\t", end='', file=f)
            print("\t{} = 1'b{};".format(self.out_ports[0], self.states[i]), file = f)
    def print_output_logic(self):
        print("\n/* Output Logic */",file=self.src_out);
        print("always @(state) begin\n\tcase(state)", file=self.src_out);
        print("\t\tidle:\n\t\t\tout = 1'b{};".format(self.idle['out']), file=self.src_out)
        self.out_logic(2, self.src_out)
        print("\tendcase\nend", file=self.src_out)
    
    # Generate the Verilog Source File
    def print_source(self):
        self.module_header();
        self.print_state_params();

        self.print_output_logic();
        self.next_state_logic();
        self.module_footer();

    # print the module in verilog source file input and output ports and module declaration
    def module_header(self):
        print('module {}'.format(self.source), file=self.src_out)
        if len(self.params):
            print(' #(parameter ', file=self.src_out, end='')
            for i in range(len(self.params)-1):
                print(self.params[i], file = self.src_out, end=', ')
            print(self.params[-1], end=')\n', file=self.src_out)
        print('(', file=self.src_out)
        for port in self.in_ports:
            print('\tinput wire {}'.format(port), end=',\n', file=self.src_out)
        for i in range(len(self.out_ports)-1):
            print('\toutput reg {}'.format(out_ports[i]), end=',\n', file=self.src_out)
        print('\toutput reg {}\n);'.format(self.out_ports[-1]),file=self.src_out)
    
    # print end module in verilog source file
    def module_footer(self):
        print('endmodule', file=self.src_out)

