# babyre
Re

## Challenge 

Welcome to reverse engineering

Recommended reading:

	x86 Crash Course - https://www.youtube.com/watch?v=75gBFiFtAb8
	Introduction to x86 (Strongly encouraged) - https://www.youtube.com/playlist?list=PL038BE01D3BAEFDB0
	Ghidra Quick Start - https://www.youtube.com/watch?v=fTGTnrgjuGA
	Calling convention for x86 64 bit - https://wiki.osdev.org/Calling_Conventions#Cheat_Sheets
	The Introduction to x86 playlist covers concepts for 32-bit, but our challenges will be in 64-bit (because its 2019 already). They are roughly the same, but take note of the calling convention. You can compile a test program to find out.

Author: daniellimws

## Solution

Decompile in Hopper

	int main() {
	    printf("Enter flag: ");
	    scanf("%256s");
	    if (strcmp(&var_108, "HATS{so_easy}") == 0x0) {
	            printf("%s is the flag\n", &var_108);
	    }
	    else {
	            puts("SO NOOB");
	    }
	    rax = 0x0;
	    rdx = *0x28 ^ *0x28;
	    if (rdx != 0x0) {
	            rax = __stack_chk_fail();
	    }
	    return rax;
	}

## Flag

	HATS{so_easy}
