Description
-----------
The python program takes a configuration file describing a State Machine and genertes a source file and a verilog testbench file for the same.

How to Run
----------
To generate the source file:
	./main.py -s sm_conf -m module_name
To compile the verilog file using icarus verilog
	iverilog -o output module.v tb.v
	vvp output
To view the waveform in gtkwave
	gtkwave test/test.vcd

