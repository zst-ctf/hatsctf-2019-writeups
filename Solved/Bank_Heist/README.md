# Bank Heist
Web

## Challenge 

Money in the bank. Gotta withdraw all of it! Can you deposit more than $1337?

http://challs.hats.sg:1347/

Flag format: flag{.+}

Challenge by: Gladiator

## Solution

Use inspect elements to change the value to 1337

	<option value="1">$1</option>

Change to 

	<option value="1337">$1</option>

## Flag

	flag{5555555555555_I_told_you_input_validation_important!!!!5555555}
