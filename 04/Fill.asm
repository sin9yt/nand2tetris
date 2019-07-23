// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.
(BEGIN)
@SCREEN
D = A
@R0
M = D 
@KBD
D = M
@MAKEBLACK
D; JNE
@MAKEWHITE
D; JEQ

(MAKEBLACK)
@SCREEN
M = -1
(LOOPBLACK)
@R0
AMD = M + 1
M = -1
@24576
D = A - D
D = D - 1
@LOOPBLACK
D; JGT
@BEGIN
0; JMP

(MAKEWHITE)
@SCREEN
M = 0       // Set RAM[16384] to 0
(LOOPWHITE)
@R0
AMD = M + 1
M = 0
@24576
D = A - D
D = D - 1   // Whiten till RAM[24575]
@LOOPWHITE
D; JGT      // if(D < 24575) goto LOOPWHITE
@BEGIN
0; JMP      // goto beginning to check keyboard input