`timescale 1ns/1ns

`define CYCLE 10
`define module_name source
`define test_in  "test/test.in"
`define test_out  "test/test.out"
`define wave_out  "test/test.vcd"

module main;

reg in, x;
reg reset_n;
wire out;
reg clock;

integer fin, fout, count;

/* Design Under Test */
`module_name dut (.clock(clock), .in(in), .x(x), .reset_n(reset_n), .out(out));

initial begin
 clock = 1'b0;
 forever begin
	#(`CYCLE/2) clock = 1'b1;
	#(`CYCLE - `CYCLE/2) clock = 1'b0;
 end
end

initial begin
	$dumpfile(`wave_out);
	$dumpvars(0, main);
end

initial begin 
	in = 1'b0;
	x = 1'b0;
	reset_n = 1'b0;
	fin = $fopenr(`test_in);
	fout = $fopenw(`test_out);
	if(!fin || !fout) begin
		$display("Can't Open files");
		$finish();
	end
	while (!$feof(fin)) begin
		@(negedge clock) reset_n = 1'b1;
		count = $fscanf(fin, "%b %b", in, x);
	end
	$fclose(fin);
	$fclose(fout);
	$finish();
end
always @(posedge clock) begin
	if(reset_n)
		$fwrite(fout, "%b\n", out);
end
endmodule

