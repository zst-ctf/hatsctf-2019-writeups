# noasm
Re

## Challenge 

It's easier if we have the source code, don't you think?

Author: daniellimws

## Solution

Format the code using this online beautifier website:

https://codebeautify.org/python-formatter-beautifier

Now we can extract the main if-statements...

	if (len(pw) != 19)
	if (int(('0x' + p), 0) != 310333690747)
	if (b != ''.join(map(chr, [89, 88, 78, 116, 88, 119, 61, 61])))
	if (h != '109dd7decb2e3a3658db75dcad688658')
	if (r != random.randint(0, 100))

And we can see the assignment of global variables

	for __g['rs'] in [([87, 16, 33, 1, 56, 73])]][0])
	for __g['h'] in [(hashlib.md5(pw[9: 13]).hexdigest())]][0])
	for __g['b'] in [(base64.b64encode(pw[5: 9]))]][0])
	for __g['p'] in [(binascii.hexlify(pw[0: 5]))]][0])
	for __g['pw'] in [(raw_input())]][0])[1]

	 for __g['c'] in [(pw[i])]
	 for (__g['i'], __g['r']) in [(__i)]
	 [(random.seed(c), (lambda __after: (__print('WRONG4'), (exit(0), __after())[1])[1]
	 if (r != random.randint(0, 100))

	if __i is not __sentinel
	            else __after())(next(__items, __sentinel)))())(iter(zip(range(13, 19), rs)), lambda: (__print("That's the flag, go submit it."), __after())[1], [])
	            

Hence, we know that the following

	#1: pw
		Password length is 19

	#2: p
		Decimal to Hex to ASCII
		310333690747 -> 0x484154537B -> 'HATS{'

	#3: b
		Base64 decode
		>>> import base64
		>>> enc = ''.join(map(chr, [89, 88, 78, 116, 88, 119, 61, 61]))
		>>> base64.b64decode(enc)
		'asm_'

	#4: h
		Reverse hash md5 using crackstation.net
		109dd7decb2e3a3658db75dcad688658    md5    is_e

	#5: r
		Do a random.seed(pw[i]) for i = 13 to 19 exclusive.
		random.randint(0, 100) will produce the following results:
		  [87, 16, 33, 1, 56, 73]

		Bruteforce seed and get the flag

Run the following script for #5

```python
import string
results = [87, 16, 33, 1, 56, 73]
seeds = []
for i in range(6):
	for ch in string.printable:
		random.seed(ch)
		if random.randint(0, 100) == results[i]:
			seeds.append(ch)
			break

print(seeds)

>>> ['a', '0', 'i', 'e', 'r', '}']

```

Put all together

	noasm $ python2 noasm.py
	Tell me the flag and I will let you know if you are right: HATS{asm_is_ea0ier}
	That's the flag, go submit it.

Flag does not work, it is a false positive

	noasm $ python2 noasm.py
	Tell me the flag and I will let you know if you are right: HATS{asm_is_easier}
	That's the flag, go submit it.

## Flag

	HATS{asm_is_easier}
