`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: simi sai engineer
//
// Create Date:   21:30:25 02/18/2022
// Design Name:   pipelined_regfile_5stage
// Module Name:   Y:/CX3001_Lab3p1/testbench_5_stage_pipeline.v
// Project Name:  CX3001_Lab3
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: pipelined_regfile_5stage
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module testbench_5_stage_pipeline;

	// Inputs
	reg clk;
	reg rst;

	// Outputs
	wire [63:0] PCOUT;
	wire [31:0] INST;
	wire [63:0] rdata1;
	wire [63:0] rdata2;
	wire [63:0] rdata1_ID_EXE;
	wire [63:0] rdata2_ID_EXE;
	wire [63:0] imm_ID_EXE;
	wire [63:0] rdata2_imm_ID_EXE;
	wire [2:0] aluop_ID_EXE;
	wire alusrc_ID_EXE;
	wire [4:0] waddr_ID_EXE;
	wire [63:0] aluout;
	wire [4:0] waddr_EXE_MEM;
	wire [63:0] aluout_EXE_MEM;
	wire [63:0] rdata2_EXE_MEM;
	wire [63:0] dmemdata;
	wire [4:0] waddr_MEM_WB;
	wire [63:0] aluout_MEM_WB;
	wire [63:0] wdata_WB;

	// Instantiate the Unit Under Test (UUT)
	pipelined_regfile_5stage uut (
		.clk(clk), 
		.rst(rst), 
		.PCOUT(PCOUT), 
		.INST(INST), 
		.rdata1(rdata1), 
		.rdata2(rdata2), 
		.rdata1_ID_EXE(rdata1_ID_EXE), 
		.rdata2_ID_EXE(rdata2_ID_EXE), 
		.imm_ID_EXE(imm_ID_EXE), 
		.rdata2_imm_ID_EXE(rdata2_imm_ID_EXE), 
		.aluop_ID_EXE(aluop_ID_EXE), 
		.alusrc_ID_EXE(alusrc_ID_EXE), 
		.waddr_ID_EXE(waddr_ID_EXE), 
		.aluout(aluout), 
		.waddr_EXE_MEM(waddr_EXE_MEM), 
		.aluout_EXE_MEM(aluout_EXE_MEM), 
		.rdata2_EXE_MEM(rdata2_EXE_MEM), 
		.dmemdata(dmemdata), 
		.waddr_MEM_WB(waddr_MEM_WB), 
		.aluout_MEM_WB(aluout_MEM_WB), 
		.wdata_WB(wdata_WB)
	);
	
	
	// toggles clock every 15 ns
	always #15 clk = ~clk;

	initial begin
		// Initialize Inputs
		clk = 0;
		rst = 0;

		// Wait 100 ns for global reset to finish
		#100;
        
		// Add stimulus here
		#25 rst = 1;
		#25 rst = 0;

	end
      
endmodule

