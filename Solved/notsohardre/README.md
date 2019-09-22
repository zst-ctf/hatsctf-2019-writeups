# notsohardre
Re

## Challenge 

This time it's really reverse engineering, but not the hard part yet.

Recommended reading:

The previous challenges may not need it, but it is very helpful to use a debugger. The debugger for Linux binaries is GDB. Here are nice walkthroughs of a CTF challenge using GDB. https://www.youtube.com/watch?v=o0od6i3uZFA or https://www.youtube.com/watch?v=VroEiMOJPm8
GEF is a nice extension to GDB https://github.com/hugsy/gef
You can dump memory to a file during runtime https://sourceware.org/gdb/onlinedocs/gdb/Dump_002fRestore-Files.html
You can create a file with lines of GDB commands and execute them at once in GDB. This allows for some scripting, which may be helpful for this challenge. https://sourceware.org/gdb/onlinedocs/gdb/Command-Files.html

Author: daniellimws

## Hint
When you see complicated functions while doing reverse engineering, it is possible that it is a known algorithm. Try searching in Google some of the constants used, who knows you may find something. Or look around past CTF writeups, there could be things that are similar in this program.

## Solution

Decompile in Ghidra

	undefined8 FUN_00101601(void)
	{
	  int iVar1;
	  size_t sVar2;
	  long in_FS_OFFSET;
	  int local_13c;
	  undefined local_138 [16];
	  char local_128 [264];
	  long local_20;
	  
	  local_20 = *(long *)(in_FS_OFFSET + 0x28);
	  FUN_001008ea();
	  printf("Enter the password: ");
	  __isoc99_scanf("%255s",local_128);
	  sVar2 = strlen(local_128);
	  if (sVar2 == 0x2c) {
	    local_13c = 0;
	    while( true ) {
	      sVar2 = strlen(local_128);
	      if (sVar2 <= (ulong)(long)local_13c) break;
	      FUN_001013bf((ulong)(uint)(int)local_128[(long)local_13c],local_138,local_138);
	      iVar1 = memcmp(local_138,&DAT_00302040 + (long)local_13c * 0x10,0x10);
	      if (iVar1 != 0) {
	        puts("WRONG");
	        goto LAB_0010172e;
	      }
	      local_13c = local_13c + 1;
	    }
	    puts("YOU GOT IT!");
	  }
	  else {
	    puts("WRONG");
	  }
	LAB_0010172e:
	  if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) {
	                    /* WARNING: Subroutine does not return */
	    __stack_chk_fail();
	  }
	  return 0;
	}

We see that it does some calculations in FUN_001013bf(), before doing a memcmp().

We can [hijack memcmp through the use of LD_PRELOAD](https://www.exploit-db.com/papers/13233).

	# gcc -fPIC -c memcmp-hijack.c -o memcmp-hijack.o
	# gcc -shared -o memcmp-hijack.so memcmp-hijack.o
	# LD_PRELOAD="./memcmp-hijack.so" ./notsohardre

From the output, it looks like memcmp is called 44 times. Furthermore, I filled in the flag format header and those chars that match the flag format are equal in value for ptr1 and ptr2.

	# LD_PRELOAD="./memcmp-hijack.so" ./notsohardre
	Enter the password: HATS{aaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaa
	 -> start memcmp
	 -> ptr1: 41 58 8D 5D 68 18 A2 A6 7B 88 32 30 76 34 52 F6 
	 -> ptr2: 41 58 8D 5D 68 18 A2 A6 7B 88 32 30 76 34 52 F6 
	 -> end memcmp
	 -> start memcmp
	 -> ptr1: 1C 84 D3 70 6A CD 2D 59 EC 6B 68 79 17 23 A0 11 
	 -> ptr2: 1C 84 D3 70 6A CD 2D 59 EC 6B 68 79 17 23 A0 11 
	 -> end memcmp
	 -> start memcmp
	 -> ptr1: D4 33 96 B6 9B 07 7C 6A BF BC 9C C0 A1 74 7C 29 
	 -> ptr2: D4 33 96 B6 9B 07 7C 6A BF BC 9C C0 A1 74 7C 29 
	 -> end memcmp
	 -> start memcmp
	 -> ptr1: 40 AF 92 01 55 7D B9 C7 92 37 DA 41 CC BF 23 45 
	 -> ptr2: 40 AF 92 01 55 7D B9 C7 92 37 DA 41 CC BF 23 45 
	 -> end memcmp
	 -> start memcmp
	 -> ptr1: D5 F6 28 78 DC 36 9E 93 61 4F E0 D6 C2 25 72 71 
	 -> ptr2: D5 F6 28 78 DC 36 9E 93 61 4F E0 D6 C2 25 72 71 
	 -> end memcmp
	 -> start memcmp
	 -> ptr1: C8 D2 FC AE B4 BC B2 84 FD 73 12 61 FE CF 0E C3 
	 -> ptr2: 0E 74 CD 43 CF C5 D4 8D 27 2F 37 16 BB B8 99 C8 
	 -> end memcmp
	 ...

If you look at the decompiled code, it also checks for a string length of 44. Hence, I conclude that each pair of ptr1 and ptr2 are for each char of the flag.

	  printf("Enter the password: ");
	  __isoc99_scanf("%255s",local_128);
	  sVar2 = strlen(local_128);
	  if (sVar2 == 0x2c) {
	  	//...
	  }
	  else {
	    puts("WRONG");
	  }

If we bruteforce until the ptr1 and ptr2 matches, we will get each char of the flag.

	# python3 solve.py 
	Progress HATS{you_didnt_really_reverse_this_did_you?}
	Success HATS{you_didnt_really_reverse_this_did_you?}

## Flag

	HATS{you_didnt_really_reverse_this_did_you?}
