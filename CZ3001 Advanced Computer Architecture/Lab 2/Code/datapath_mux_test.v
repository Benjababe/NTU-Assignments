`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   14:02:15 02/07/2022
// Design Name:   datapath_mux
// Module Name:   Y:/CX3001_lab2/datapath_mux_test.v
// Project Name:  CX3001_lab2
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: datapath_mux
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module datapath_mux_test;

	// Inputs
	reg clk;
	reg rst;
	reg [31:0] inst;

	// Outputs
	wire [63:0] aluout;

	// Instantiate the Unit Under Test (UUT)
	datapath_mux uut (
		.clk(clk), 
		.rst(rst), 
		.inst(inst), 
		.aluout(aluout)
	);
	
	// toggle clock every 15ns
	always #15 clk = ~clk;

	initial begin
		// Initialize Inputs
		clk = 0;
		rst = 0;
		inst = 0;

		// Wait 100 ns for global reset to finish
		#100;
        
		// Add stimulus here
		#10 rst = 1;
		#50 rst = 0;
		
		// wait 50ns for global reset to finish
		#50; 
		
		// ADD X3, X1, X4
		#100 inst = 32'h00040023;
		
		// SUB X4, X1, X2
		#100 inst = 32'h00220024;
		
		// AND X7, X1, X4
		#100 inst = 32'h00440027; 
		
		// XOR X8, X7, X2
		#100 inst = 32'h006200E8; 
		
	end
      
endmodule

