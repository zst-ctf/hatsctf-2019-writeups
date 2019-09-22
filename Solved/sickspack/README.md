# sickspack
Re

## Challenge 

Doing CTFs makes your six pack gone

Recommended reading:

https://blog.malwarebytes.com/cybercrime/malware/2017/03/explained-packer-crypter-and-protector/
https://en.wikipedia.org/wiki/Self-modifying_code
https://sourceware.org/gdb/onlinedocs/gdb/Dump_002fRestore-Files.html
Author: daniellimws
## Solution

Reference: https://medium.com/@monliclican/rootcon-2017-ctf-binforcry-350-write-up-walkthrough-part-2-of-x-5731c91c2266

The UPX! strings indicate that the file was packed using UPX. UPX — or Ultimate Packer for Executables — is one of the most famous packers out there.

	$ strings sickspack | tail
	ymro
	H3$1
	?H6!
	UPX!
	UPX!

Unpack the executable.

	# sudo apt-get install -y upx

	# upx -d sickspack -o sickspack_unpacked
						   Ultimate Packer for eXecutables
							  Copyright (C) 1996 - 2018
	UPX 3.95        Markus Oberhumer, Laszlo Molnar & John Reiser   Aug 26th 2018

			File size         Ratio      Format      Name
	   --------------------   ------   -----------   -----------
		 18240 <-      6384   35.00%   linux/amd64   sickspack_unpacked

	Unpacked 1 file.

---

Now we can decompile in Hopper.

	int main() {
		printf("Enter flag: ");
		__isoc99_scanf(0x19e8, &var_48);
		if (fun("``amml0`ammf06becaamm7eag`gmeeeeeeammla`3mfd6eamm7ebamm1a17m6ba`7g`3cfbaccamml64ammla`7mamm7abemammla`6eamm7abdeammla`6mamm7abdmammla`1eamm7abgeammla`1mamm7abgmammla`0eamm7abfeammla`0mamm7abfmammla`3eam7mamad`a`fb7c0c3`3ammla`l4am7mc1febgff`3fcbecdammla`4g…", &var_48) != 0x0) {
				puts("YOU GOT IT!");
		}
		else {
				puts("WRONG!");
		}
		rax = 0x0;
		rdx = *0x28 ^ *0x28;
		if (rdx != 0x0) {
				rax = __stack_chk_fail();
		}
		return rax;
	}

	int fun(int arg0, int arg1) {
		var_18 = arg0;
		var_20 = arg1;
		var_8 = fun;
		for (var_10 = 0x66; var_10 <= 0x87; var_10 = var_10 + 0x1) {
			*(int8_t *)(var_10 + fun) = 
				*(int8_t *)(var_10 + fun) & 0xff ^ *(int8_t *)(var_10 + 0x2022fa) & 0xff; // diff == 0x2022fa
		}
		rax = puts("SIKED");
		rax = puts("DO YOU KNOW THE FLAG?");
		rax = puts("WHAT ARE YOU DOING HERE?");
		rax = puts("GO HOME");
		rax = puts("YOU ARE BAD");
		rax = puts("WHAT'S THE POINT OF READING THIS?");
		rax = puts("DELETE THIS PROGRAM");
		rax = puts("QUIT THE CTF");
		return rax;
	}

From the code of fun(), we know that it ***modifies itself upon runtime***. (From `fun+0x66` to `fun+0x87`).

We can get a disassembly in GDB during runtime...

	(gdb) break puts

	(gdb) run

	(gdb) x/20i fun+0x66
	   0x5555555557d0 <fun+102>:	lea    0x200849(%rip),%rax        # 0x555555756020 <real>
	   0x5555555557d7 <fun+109>:	mov    %rax,-0x8(%rbp)   // var_8 = real
	   0x5555555557db <fun+113>:	mov    -0x20(%rbp),%rcx  // rcx = var_20
	   0x5555555557df <fun+117>:	mov    -0x18(%rbp),%rdx  // rdx = var_18
	   0x5555555557e3 <fun+121>:	mov    -0x8(%rbp),%rax   // rax = var_8
	   0x5555555557e7 <fun+125>:	mov    %rcx,%rsi         // rsi = rcx == var_20 // param2
	   0x5555555557ea <fun+128>:	mov    %rdx,%rdi         // rdi = rdx == var_18 // param1
	   0x5555555557ed <fun+131>:	callq  *%rax             // call real(var_18, var_20)
	   0x5555555557ef <fun+133>:	nop
	   0x5555555557f0 <fun+134>:	leaveq 
	   0x5555555557f1 <fun+135>:	retq   

And here, we can see that it calls a function called real().

We can decompile the memory and see the instructions. We see some code at the bottom of real.

	(gdb) x/100i  &real
	<snipped>

	   0x555555756110 <code+48>:	mov    %rax,-0x40(%rbp)
	   0x555555756114 <code+52>:	mov    0x10(%rdi),%rax
	   0x555555756118 <code+56>:	mov    %rax,-0x38(%rbp)
	   0x55555575611c <code+60>:	mov    0x18(%rdi),%rax
	   0x555555756120 <code+64>:	mov    %rax,-0x30(%rbp)
	   0x555555756124 <code+68>:	mov    0x20(%rdi),%rax
	   0x555555756128 <code+72>:	mov    %rax,-0x28(%rbp)
	   0x55555575612c <code+76>:	mov    0x28(%rdi),%rax
	   0x555555756130 <code+80>:	mov    %rax,-0x20(%rbp)
	   0x555555756134 <code+84>:	mov    0x30(%rdi),%rax
	   0x555555756138 <code+88>:	mov    %rax,-0x18(%rbp)
	   0x55555575613c <code+92>:	mov    0x38(%rdi),%rax
	   0x555555756140 <code+96>:	mov    %rax,-0x10(%rbp)
	   0x555555756144 <code+100>:	movabs $0x5f6f6e7b53544148,%rax
	   0x55555575614e <code+110>:	mov    %rax,-0x66(%rbp)
	   0x555555756152 <code+114>:	movabs $0x6170365f3372306d,%rax
	   0x55555575615c <code+124>:	mov    %rax,-0x5e(%rbp)
	   0x555555756160 <code+128>:	movabs $0x72657466615f6b63,%rax
	   0x55555575616a <code+138>:	mov    %rax,-0x56(%rbp)
	   0x55555575616e <code+142>:	mov    $0x7d,%eax

We see the last 3 integers are huge and suspicious

Let's print it out

	>>> from pwn import *
	>>> p64(0x5f6f6e7b53544148)
	'HATS{no_'
	>>> p64(0x6170365f3372306d)
	'm0r3_6pa'
	>>> p64(0x72657466615f6b63)
	'ck_after'
	>>> p64(0x7d)
	'}'

Unfortunately `HATS{no_m0r3_6pack_after}` is not the (full) flag.

From the disassembly, the flag should be stored in the memory. Let's do an easier method by dumping the memory.

	(gdb) break puts
	Breakpoint 1 at 0x1610
	
	(gdb) run
	Starting program: /FILES/sickspack_unpacked 
	Enter flag: 123

	Breakpoint 1, _IO_puts (str=0x5555555559f9 "WRONG!") at ioputs.c:33
	33	ioputs.c: No such file or directory.
	
	(gdb) print $rbp
	$1 = (void *) 0x7fffffffec00
	
	(gdb) dump binary memory result.bin 0x7fffffff0000 0x7fffffffec00

Now we can read the memory dump

	$ strings result.bin | grep HATS
	HATS{no_m0r3_6pack_after_ctf}

## Flag

	HATS{no_m0r3_6pack_after_ctf}
