`include"define.v"
`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////////
//// Company: NTU
//// Engineer: Dr. Smitha K G
////////////////////////////////////////////////////////////////////////////////////

module datapath_mux (
	// inputs
	clk,
	rst,
	inst,

	//outputs
	aluout
);

// inputs
input		  clk;
input		  rst;
input  [`ISIZE-1:0] inst;


// outputs
output  [`DSIZE-1:0] aluout;

wire [2:0]	aluop;

wire wen;
wire [`DSIZE-1:0] rdata1;
wire [`DSIZE-1:0] rdata2;





//Here you need to instantiate the control , Alu ,and regfile. 
//The codes below are not given to students.

//-insert your code here





endmodule // end of datapath module

