Description
-----------
The python program takes a configuration file describing a State Machine and genertes a source file and a verilog testbench file for the same.

How to Run
----------
To generate the source file:<br>
	./main.py -s sm_conf -m module_name<br>
To compile the verilog file using icarus verilog<br>
	iverilog -o output module.v tb.v<br>
	vvp output<br>
To view the waveform in gtkwave<br>
	gtkwave test/test.vcd<br>

