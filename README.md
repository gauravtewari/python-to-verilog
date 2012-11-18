# Description
The python program takes a configuration file describing a State Machine and genertes a source file and a verilog testbench file for the same.

# How to Run

**Verilog Source File Generation**  &mdash; *To generate the source file `module` is the name of the module as well as the generated verilog file*

	./main.py -s sm_conf -m module_name<br>

**Compile Using IVerilog** &mdash; *To compile the verilog file using icarus verilog*
Modify the testbench file `tb.v` to update the module DUT name, the file name where to read the input stimulus data and the file name where to store the generated output

	iverilog -o output module.v tb.v
	vvp output

**View the waveform** &mdash; *To view the waveform in gtkwave*

	gtkwave test/test.vcd<br>

