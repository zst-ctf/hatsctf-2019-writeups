# BabyCrypto
Crypto

## Challenge 

Welcome to crypto!

This challenge is just a simple challenge to get you started with crypto.

Crypto resources:

Google! Google for keywords that you think are related and try to find resources. Stack overflow and papers are usually good resources
Wikipedia, it gives you a basic idea of the algorithm/attack and more sources that you can look after, paywalled papers can be bypassed with sci-hub
Sage. This is basically a python-based language that is very powerful in (abstract) algebra and number theory. Don't be scared with so many functions with confusing names, look for functions that you need. Try out the code provided in the sage documentation too
Cryptopals, this is more for the logic kind of attack ideas, useful to see how attacks are realized for crypto especially block ciphers/hashes
WIP book more on the math-ey side of crypto, the current book can be found here: https://ariana1729.github.io/Books/Cryptography and attacks/Book.pdf
Challenge by: Ariana

## Hint
Remember the flag format?

XOR and addition is reversible, try to bruteforce k1/k2

## Solution

Explanation of chal.py

- get random numbers k1 and k2

- for each char in flag, add k2 then xor k1

From the hint, we can bruteforce and reverse the flag.


## Flag

	HATS{b451c_cryp74n4ly515}
