# HeapSchool
Pwn

## Challenge 

	Pop quiz time!

	*Note: This challenge can be solved without reversing the binary. In fact, I suggest not using the binary as it will mostly waste your time.

	nc challs.hats.sg 1305

	Recommended Reading:

	https://heap-exploitation.dhavalkapil.com/
	https://azeria-labs.com/heap-exploitation-part-1-understanding-the-glibc-heap-implementation/
	https://github.com/shellphish/how2heap
	Author: Lord_Idiot

## Hint

## Solution

Reference:

- https://stackoverflow.com/questions/24359138/malloc-storing-its-metadata

For Section A, 

- Malloc heap size is in multiples of 0x10.
- Include the metadata size, then round up in multiples of 0x10.


For Section B,

- The address given is the integer "if previous chunk is free, this field contains size of previous chunk."
- simply convert the previous chunk's size into hex and submit.

As follows:

	Welcome to Heap School!
	We'll be starting class with a pop quiz!
	Note: This challenge is based on the Ubuntu 16.04 [64-bit] ptmalloc allocator (Ubuntu GLIBC 2.23-0ubuntu11)

	##################### SECTION A #####################
	Q1: I call malloc(60),
	What is the actual chunk size, including chunk metadata?
	(e.g. 1337): 80
	Correct! ✓

	Q2: I call malloc(15),
	What is the actual chunk size, including chunk metadata?
	(e.g. 1337): 32
	Correct! ✓

	Q3: I call malloc(76),
	What is the actual chunk size, including chunk metadata?
	(e.g. 1337): 96
	Correct! ✓

	Congrats! You have completed [SECTION A]
	################# END OF SECTION A ##################

	##################### SECTION B #####################
	Heap base is current at: 0x0000558057c65000
	malloc(497) = 0x0000558057c65010
	malloc(481) = 0x0000558057c65210
	malloc(301) = 0x0000558057c65400

	Q1: What is the QWORD value at 0x0000558057c65208?
	(e.g. 0xdeadbeef): 0x000001f1
	Correct! ✓

	Q2: What is the QWORD value at 0x0000558057c65208?
	(e.g. 0xdeadbeef): 0x000001f1
	Correct! ✓

	Congrats! You have completed [SECTION B]
	################# END OF SECTION B ##################

	Congrats! Here is your flag: HATS{You_get_an_A!}

## Flag

	HATS{You_get_an_A!}
