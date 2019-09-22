#!/usr/bin/env python3
c = [194, 203, 222, 221, 53, 44, 254, 255, 251, 45, 41, 45, 60, 51, 58, 241, 254, 56, 254, 38, 51, 255, 251, 255, 55]
for k1 in range(0, 0x100):
    for k2 in range(0, 0x80):
        try:
            msg_int = list(map(lambda ch: (ch^k1) - k2, c))
            msg = ''.join((map(chr, msg_int)))
            if 'HATS{' in msg:
                print(msg)
        except:
            pass
