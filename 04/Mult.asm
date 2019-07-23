// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
(BEGIN)
@R2
M = 0   // Initialize R2 to 0

(LOOP)
@R1
D = M - 1
@NULL
D; JLT

@R0
D = M
@R2
D = D + M
M = D
@R1
M = M - 1
D = M
@LOOP
D; JGE

(NULL)
@R0
M = 0