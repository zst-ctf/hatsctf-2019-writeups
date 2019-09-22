# AES-RSA
Crypto

## Challenge 

I've made a combination of AES and RSA for my new crypto scheme. I may have forgotten how to decode RSA, could you help me retrieve the flag?

nc challs.hats.sg 1401

Challenge by: Ariana

## Hint

Here you have a padding oracle

What happens when the message and exponent is small in rsa?

## Solution

From the code:

- Provide a message: m
- First, RSA encrypt: n = random, e = 3
- Second, AES CBC encrypt: iv = random, key = random (same across instance)

Attack method:

1. Padding oracle attack on AES CBC because decrypt shows us if successful (0) or failure (-1). This will provide us with RSA(m, e, N).
2. From the hint, the message and exponent is small. Hence if m^e is smaller than N, that means we can simply cube root (e = 3) the ciphertext to get the plaintext

But because there is a limit of 0x2000 attempts, it is rather tight and often we may exceed the attempts.

So I had to run the script a few times to be lucky and be under the attempt limit.

---

When I got the final RSA, I could not decrypt it. I forgot to unpad the message from the AES decrypted text.

	Final P: b'\x05\xc1\x8e\xd8!\xa2\x93\x0fb\x84\x11\x9a\xf9\x12-\xad~\xbb\xe7\t\xe5\xb1X\t\x83\xfb\xb0\xed\xc0\xb5X\xfb0\x9e\x9a\x02a\x86!\xc4\xfe\x93\x99\xdfk\x86is\xcd\x104\xdc\xfc\xd4\x14\x0f\\\x0c\te\x04\x04\x04\x04'
	Final P: 05c18ed821a2930f6284119af9122dad7ebbe709e5b1580983fbb0edc0b558fb309e9a02618621c4fe9399df6b866973cd1034dcfcd4140f5c0c096504040404
	False b'\x01\xca\xca\xb8xFa\xa6\xf2\x1cq\xd6\xce\n\x8cf|\xd68\xfa\xedF'

After unpadding it, I got the flag.

	Unpad P: b'\x05\xc1\x8e\xd8!\xa2\x93\x0fb\x84\x11\x9a\xf9\x12-\xad~\xbb\xe7\t\xe5\xb1X\t\x83\xfb\xb0\xed\xc0\xb5X\xfb0\x9e\x9a\x02a\x86!\xc4\xfe\x93\x99\xdfk\x86is\xcd\x104\xdc\xfc\xd4\x14\x0f\\\x0c\te'
	Unpad P: 05c18ed821a2930f6284119af9122dad7ebbe709e5b1580983fbb0edc0b558fb309e9a02618621c4fe9399df6b866973cd1034dcfcd4140f5c0c0965
	True b'HATS{f14g_t00_sh0rt}'

## Flag

	HATS{f14g_t00_sh0rt}
