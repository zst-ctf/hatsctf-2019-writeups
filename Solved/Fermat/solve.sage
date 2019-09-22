#!/usr/bin/env sage

n = 0x6216bfea994a31f3a352e8f162b1b6896025ba91188a458daa0aa758d4ecb595089aaa379a8b3c2c1bde708e6bbb0fa99dce996b8d9f259e319c881e41bc8635d348c6004325dae4d3a6bfe78e62499f819cd9bd74686943c7cbe9b68372bb43dc375341bae69120ee763cb282ddf0f117a150aa3c862bdad372401220caa3a1fb1dd6c369d4d5dbd78f15f40e0bbebb6f3fa123a5756d10fb62e49f7c73aa171b007a281de6910dfc67aae5a691c3329a5c64700b0b54ceaeaa95639c6030925f190f587f53ee9d718e0e7dfa2b059b1a6a701620b058498cd2c2ebeac76153150b8886fcfc99d35d10139f9d364c7393c70181569e2269d5ff214d5e6a253
c = 0x725f17256760e05a02359447947aeb7d83fa7350408dc1abb1ba03ff9e1c15167171c6f493620005ac5e2c641912e5c09cbeea9fed542bf7dbd8016bf3ce5758bf83f1d941b8926992816912e47a62344c4d0ca068a071933c98300a073930be59f051cda8bc8fc69e61a490090a95c18380877c73b230b4a65ecb676bcfa0a7b2d8ce61a6857b822bea9304686e6393f03040489926e940e1f098fdd9ceb74d54e972625141bc7fb322c68bb00f27c030286c1d1e71e861f70ff08c17d5461261ee44614c6fb94e5490d86669f6b9af6fd6a141cb0c39ac692e7d51f3ab28bd71b3b5502c5be6ebbec6622065ce60be64247e7cd2298c746716fc686981f7
e = 65537

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

print("p = " + str(p))
print("q = " + str(q))

assert (p*q) == n

def RSA_Decrypt(p, q, e, c):
	# Compute phi
	phi = (p-1) * (q-1)

	# Compute modular inverse of e
	d = inverse_mod(e, phi)

	# Decrypt ciphertext
	m = pow(c, d, n)

	# convert to ascii
	m_hex = hex(int(m)).lstrip('0x').rstrip('L')
	m_str = ('0'*(len(m_hex) % 2) + m_hex).decode('hex')
	print(m_str)

RSA_Decrypt(p, q, e, c)
