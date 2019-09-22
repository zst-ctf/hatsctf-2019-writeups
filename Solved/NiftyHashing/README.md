# NiftyHashing
Web

## Challenge 

HASH HASH HASH HASH

http://challs.hats.sg:1344/?src

http://challs.hats.sg:1344/

Do you believe you can bypass the salt?

Flag format: flag{.+}

Challenge by: Gladiator

## Solution

A trick with PHP string concatenation with arrays

See reference: https://www.pwndiary.com/write-ups/angstrom-ctf-2018-md5-write-up-web140/

Get the flag

http://challs.hats.sg:1344/?str1[]=a&str2[]=b%27

## Flag

	flag{nift_little_nifty_tricks_of_hashes_like_salt_bae}
