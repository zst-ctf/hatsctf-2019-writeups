# Residues
Crypto

## Challenge 

Without the modulus you can't possible decrypt my message right?

nc challs.hats.sg 1400

Note: you likely do not need more than 10 requests to the server

Challenge by: Ariana

## Hint

Can you obtain the modulus? Notice that if x=y(mod n), then x-y = kn

Can you factor the primes? Notice that the difference is small

Could you simplify the problem down to finding m^2 mod n?

## Solution

More explanation and reference links in the python script.

1. Read code and find out e = 65537
2. Obtain modulus using gcd(m1^e - c1, m2^e - c2)
3. Factorise modulus using Fermat factoring method.
4. Decrypt

## Flag

	HATS{50m3_r351du3_l3f7}
