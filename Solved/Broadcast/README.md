# Broadcast
Crypto

## Challenge 
You have managed to force alice to resend her ciphertext multiple times. Can you recover the message?

Challenge by: Ariana

## Hint

Notice that only n is changing, m and e are fixed. Is there any attack for such a case?

## Solution

Find out the exponent.

	$ python3
	>>> from gmpy2 import next_prime
	>>> e = next_prime(9**3)
	>>> e   
	mpz(733)

e = 733, but only 81 messages given. 

To do Hastad's broadcast attack, the number of messages must be at least the value of the exponent.

However for some reason, it is still sufficient to do Hastad's broadcast attack

Adapt code from https://github.com/ashutosh1206/Crypton/blob/master/RSA-encryption/Attack-Hastad-Broadcast/hastad_unpadded.py

## Flag

	$ python2 test.py 
	HATS{3xp0n3n7_700_5m41l!!!}
