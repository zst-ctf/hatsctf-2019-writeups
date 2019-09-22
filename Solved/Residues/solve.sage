#!/usr/bin/env sage
import socket
import telnetlib

# Connect to program
s = socket.socket()
s.connect(('challs.hats.sg', 1400))

t = telnetlib.Telnet()
t.sock = s

t.read_until(b'Here is the encrypted flag: ')
flag_enc = t.read_until(b'\n').strip()
flag_enc = int(flag_enc, 16)
print('Encrypted flag: ' + hex(flag_enc))

def get_cipher(numb):
    t.read_until(b'Enter a value to be encrypted:')
    t.write(hex(numb).encode() + b'\n')

    t.read_until(b'Cipher: ')
    c_hex = t.read_until(b'\n').strip()
    return int(c_hex, 16)


# Crack modulus
# https://crypto.stackexchange.com/questions/43583/deduce-modulus-n-from-public-exponent-and-encrypted-data
# https://crypto.stackexchange.com/questions/30289/is-it-possible-to-recover-an-rsa-modulus-from-its-signatures

e = 2*65537

m1 = 123
c1 = get_cipher(m1)
print('C1: ' + hex(c1))

m2 = 456
c2 = get_cipher(m2)
print('C2: ' + hex(c2))

m3 = 789
c3 = get_cipher(m3)
print('C3: ' + hex(c3))

m4 = 1111
c4 = get_cipher(m4)
print('C4: ' + hex(c4))

gcdA = gcd(pow(m1, e) - c1, pow(m2, e) - c2)
gcdB = gcd(pow(m2, e) - c2, pow(m3, e) - c3)
gcdC = gcd(pow(m4, e) - c4, pow(m3, e) - c3)

print('gcdA: ' + hex(gcdA))
print('gcdB: ' + hex(gcdB))
print('gcdC: ' + hex(gcdC))

n = gcd(gcd(gcdA, gcdB), gcdC)
print('Modulus: ' + hex(n))

# Factor modulus
# https://crypto.stackexchange.com/questions/5262/rsa-and-prime-difference
# https://en.wikipedia.org/wiki/Fermat%27s_factorization_method
# https://mathcourses.nfshost.com/archived-courses/mat-321-001-2017-fall/sage/sagecell-factorization.html

def FermatFactor(n): 
    tmin = floor(sqrt(n))+1; 

    #for t in range(tmin,n):
    t = tmin
    while t < n:
        s = sqrt(t*t - n); 
        if floor(s) == s :
            return ([t+s,t-s]);
            break;
        t += 1  

p, q = FermatFactor(n)
timeit('FermatFactor(n)')

# Square root because they are close to each other
# Does not work because they are not close enough.
'''
start = isqrt(n)
start_orig = isqrt(n)

s = 512
offset = int(2**s // 2)
start += offset

while True:
    
    p = next_prime(start)
    q = n // p

    if start > (start_orig + 2**512):
        print('Failed')
        quit()

    if (int(p * q) == int(n)):
        break
    else:
        start = p + 1
'''

# Decrypt after finding P & Q
print('P: ' + hex(p))
print('Q: ' + hex(q))

assert (int(p * q) == int(n))

# Compute phi
phi = (p-1) * (q-1)

# Compute modular inverse of e
# [Because in chall.py, they produce p and q using exponent 65537
# so we must divide e by 2]
d = inverse_mod(e // 2, phi)

# Decrypt ciphertext
pt = pow(flag_enc, d, n)

# [likewise, we must squareroot the message because e = 65537 is used
# for prime generation, but e = 2*65537 is used for encryption]
pt = isqrt(pt)

try:
    pt = (hex(pt)[2:]).decode('hex')
except:
    pt = ('0' + hex(pt)[2:]).decode('hex')

print(pt)
quit()

#######################################

t.interact()

if False:
    my_exp = 10

    m1=2^(10)+1 # or any message you want
    m2=2^(10)-1
    m3=m1^my_exp
    m4=m2^my_exp

    c1_hex = get_cipher(m1)
    c2_hex = get_cipher(m2)
    c3_hex = get_cipher(m3)
    c4_hex = get_cipher(m4)
    print('C1: ' + str(c1_hex))
    print('C2: ' + str(c2_hex))
    print('C3: ' + str(c3_hex))
    print('C4: ' + str(c4_hex))

    c1 = int(c1_hex, 16)
    c2 = int(c2_hex, 16)
    c3 = int(c3_hex, 16)
    c4 = int(c4_hex, 16)

    print('gcd', gcd(c2^my_exp-c4,c1^my_exp-c3))

    t.interact()
