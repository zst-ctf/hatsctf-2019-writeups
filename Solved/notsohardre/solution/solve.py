#!/usr/bin/env python3
from subprocess import Popen, PIPE
import os
import string

def attempt(payload):
	# Send attempt to process
	my_env = os.environ.copy()
	my_env["LD_PRELOAD"] = "./memcmp-hijack.so"
	
	cproc = Popen(["./notsohardre"],
	stdout=PIPE, stdin=PIPE, env=my_env)
	out, err = cproc.communicate(payload)

	contents = out.decode()
	# print(contents)

	# Count matching comparisons
	lines = contents.splitlines()
	match = 0
	for count in range(contents.count('start memcmp')):
		start = lines.pop(0)
		ptr1 = lines.pop(0)
		ptr2 = lines.pop(0)
		end = lines.pop(0)

		if ptr1.split(':')[1] == ptr2.split(':')[1]:
			match += 1
		# print(f'Number {count}: {match} matches')

	return match

flag = "HATS{"
flag_len = 44
current_matches = len(flag)
while len(flag) < flag_len:
	for ch in string.printable:
		payload = (flag + ch).ljust(flag_len, '\x01')
		attempted_matches = attempt(payload.encode())

		if attempted_matches > current_matches:
			current_matches = attempted_matches
			flag += ch
			print('Progress', flag)

print('Success', flag)

# attempt(b"HATS{" + b"\x01" * 39)
