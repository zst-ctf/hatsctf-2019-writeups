#!/usr/bin/env python3
import socket
import telnetlib
from math import gcd
from Crypto.Util.number import *
from Crypto.Util.Padding import pad, unpad  # pycryptodome
import gmpy2

# Connect to program
def initialise():
    global s
    global t
    global flag_enc
    global attempts

    s = socket.socket()
    s.connect(('challs.hats.sg', 1401))

    t = telnetlib.Telnet()
    t.sock = s

    t.read_until(b'recieved:\n')
    flag_enc_hex = t.read_until(b'\n').decode().strip()
    flag_enc = bytes.fromhex(flag_enc_hex)
    # flag_enc = int(flag_enc, 16)
    print('Encrypted flag: ' + flag_enc_hex)
    print('AES blocks in flag:', len(flag_enc) // 16)

    attempts = 0x2000

# API interface to server
def server_decrypt(message):
    global attempts
    attempts -= 1

    t.read_until(b'2. Decrypt service')
    t.write(b'2\n')
    # t.read_until(b'Send a message to be decrypted')
    t.write(message.encode() + b'\n')

    t.read_until(b'Decrypted message:\n')
    response = t.read_until(b'\n').decode().strip()

    #print(response, True if response == '0' else False)
    return True if response == '0' else False

def server_encrypt(number):
    global attempts
    attempts -= 1

    t.read_until(b'1. Encrypt service')
    t.write(b'1\n')
    # t.read_until(b'Send a message to be encrypted')
    message = hex(number).strip('0x')
    if len(message) % 2 == 1:
        message = '0' + message
    t.write(message.encode() + b'\n')

    t.read_until(b'Encrypted message:\n')
    response = t.read_until(b'\n').decode().strip()
    return response

# Block 0 is the IV
def get_block(message, block_number):
    b = block_number
    return message[16 * b:16 * (b + 1)]

# xor cipher on byte arrays
def xor(bytearray1, bytearray2):
    final = b''
    for a, b in zip(bytearray1, bytearray2):
        final += bytes([a ^ b])
    return final

# Padding Oracle Attack
# https://robertheaton.com/2013/07/29/padding-oracle-attack/

# We exploit this by passing in C1' + C2, where C1' is a sneakily chosen ciphertext block,
# C2 is the ciphertext block we are trying to decrypt, and C1' + C2 is the concatenation of the two.
# We call the decrypted plaintext block produced P'2.

def padding_oracle_attack(C1, C2):
    # To begin with, we choose C1'[1..15] to be random bytes, and C1'[16] to be 00.
    # We pass C1' + C2 to the server. If the server says we have produced a plaintext with valid padding,
    # then we can be pretty sure that P2'[16] must be 01 (as this would give us valid padding).
    # Of course, if the server comes back and tells us that our padding is invalid,
    # then we just set C1'[16] to 01, then 02, and so on, until we hit the jackpot.

    I2 = b''
    while len(I2) < 16:
        padding_bytes_count = len(I2) + 1
        padding_bytes = bytes([padding_bytes_count]) * padding_bytes_count

        for ch in range(256):
            # the random bytes at the start
            prepend = b'A' * (16 - padding_bytes_count)

            # the chosen byte to fit the padding
            ch = bytes([ch])

            # the already-found bytes at the end
            append = xor(I2, padding_bytes)

            # pass C1p + C2 to the server
            C1p = prepend + ch + append
            payload = C1p + C2

            print(f"\rTry length={len(I2)} ch={ch}   ", end='')
            if server_decrypt(payload.hex()):
                found_intermediate = xor(ch, padding_bytes)
                I2 = found_intermediate + I2
                print(f"\rProgress I2 = {I2}, C1p = {C1p}")
                break

    # Get plaintext of block 2
    P2 = xor(I2, C1)
    return I2, P2

'''
def get_modulus():
    e = 3

    m1 = 123
    aes_c1 = bytes.fromhex(server_encrypt(m1))
    print('aes_c1: ', (aes_c1))

    block_iv = get_block(aes_c1, 0)
    block_1 = get_block(aes_c1, 1)
    inter1, c1 = padding_oracle_attack(block_iv, block_1)
    print('c1: ', c1)

    m2 = 456
    aes_c2 = bytes.fromhex(server_encrypt(m2))
    print('aes_c2: ', (aes_c2))

    block_iv = get_block(aes_c2, 0)
    block_1 = get_block(aes_c2, 1)
    inter2, c2 = padding_oracle_attack(block_iv, block_1)
    print('c2: ', c2)

    # convert hex bytes to integers
    c1 = int(c1.hex(), 16)
    c2 = int(c2.hex(), 16)

    gcdA = gcd(pow(m1, e) - c1, pow(m2, e) - c2)
    print('gcdA: ' + hex(gcdA))
    #print('gcdB: ' + hex(gcdB))
    #print('gcdC: ' + hex(gcdC))

    n = gcdA#gcd(gcd(gcdA, gcdB), gcdC)
    print('Modulus: ' + hex(n))

    return n
'''

if __name__ == '__main__':
    #main()
    #decrypt('11')
    #decrypt(flag_enc)
    initialise()

    iv = get_block(flag_enc, 0)#.encode()
    C1 = get_block(flag_enc, 1)#.encode()
    C2 = get_block(flag_enc, 2)#.encode()
    C3 = get_block(flag_enc, 3)#.encode()
    C4 = get_block(flag_enc, 4)#.encode()
    
    I1, P1 = padding_oracle_attack(iv, C1)
    print(f"Solved I1: {I1.hex()}")
    print(f"Solved P1: {P1.hex()}")
    print(f"Attempts left: {attempts}")

    I2, P2 = padding_oracle_attack(C1, C2)
    print(f"Solved I2: {I2.hex()}")
    print(f"Solved P2: {P2.hex()}")
    print(f"Attempts left: {attempts}")

    I3, P3 = padding_oracle_attack(C2, C3)
    print(f"Solved I3: {I3.hex()}")
    print(f"Solved P3: {P3.hex()}")
    print(f"Attempts left: {attempts}")

    I4, P4 = padding_oracle_attack(C3, C4)
    print(f"Solved I4: {I4.hex()}")
    print(f"Solved P4: {P4.hex()}")
    print(f"Attempts left: {attempts}")

    Px = P1 + P2 + P3 + P4
    print(f"Final P: {Px}")
    print(f"Final P: {Px.hex()}")

    unpadded = unpad(Px, 16)
    print(f"Unpad P: {unpadded}")
    print(f"Unpad P: {unpadded.hex()}")

    Px_int = int(Px.hex(), 16)
    result, is_exact_root = gmpy2.iroot(Px_int, 3)
    print(is_exact_root, long_to_bytes(result))

    Px_int = int(unpadded.hex(), 16)
    result, is_exact_root = gmpy2.iroot(Px_int, 3)
    print(is_exact_root, long_to_bytes(result))