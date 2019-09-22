#!/usr/bin/env python3
from math import gcd

with open('data', 'r') as f:
    contents = f.read()
    contents = contents.splitlines()

c_list = []
n_list = []

for i in range(81):
	c = int(contents.pop(0))
	n = int(contents.pop(0))
	empty_line = contents.pop(0)

	c_list.append(c)
	n_list.append(n)

for i in range(81):
	for j in range(81):
		if i == j:
			continue

		n1 = n_list[i]
		n2 = n_list[j]

		factor = gcd(n1, n2)
		print(factor, n1, n2, i, j)
		if factor != 1:
			quit()
