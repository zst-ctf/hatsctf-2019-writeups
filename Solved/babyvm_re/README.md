# babyvm-re
Re

## Challenge 

You have stumbled across a interesting piece of code with seemingly random letters and numbers, can you help find what the key is?

Challenge by: Ariana

## Hint
Slowly analyse the vm, try making sense of what each instruction does

## Solution

From main(), we see that the input `key` must match that on the `stack`.

If we modify the code to print out the flag

	babyvm_re $ ./chal_modified 
	Enter the key
	k
	Verifying
	HATS{vm_r3_15_fun_r19h7?}Flag : 

## Flag

	HATS{vm_r3_15_fun_r19h7?}
