# mediumre
Re

## Challenge 

Welcome to actual re

Author: daniellimws

## Solution

Decompile in Hopper

	int main() {
	    var_18 = *0x28;
	    rax = 0x0;
	    var_138 = 0x69;
	    var_137 = 0x63;
	    var_136 = 0x77;
	    var_135 = 0x77;
	    var_134 = 0x5e;
	    var_133 = 0x47;
	    var_132 = 0x44;
	    var_131 = 0x5c;
	    var_130 = 0x5c;
	    var_12F = 0x4b;
	    var_12E = 0x47;
	    var_12D = 0x40;
	    var_12C = 0x54;
	    var_12B = 0x71;
	    var_12A = 0x5c;
	    var_129 = 0x44;
	    var_128 = 0x58;
	    var_127 = 0x5e;
	    var_126 = 0x5f;
	    var_125 = 0x6b;
	    var_124 = 0x44;
	    var_123 = 0x43;
	    var_122 = 0x5e;
	    var_121 = 0x4c;
	    var_120 = 0x5c;
	    var_11F = 0x65;
	    var_11E = 0x5e;
	    var_11D = 0x46;
	    var_11C = 0x62;
	    var_11B = 0x52;
	    var_11A = 0x5e;
	    var_119 = 0x3d;
	    rax = 0x0;
	    rax = printf("Enter flag: ");
	    rsi = &var_118;
	    rax = 0x0;
	    rax = scanf("%255s");
	    var_13C = 0x0;
	    while (sign_extend_64(var_13C) < strlen(&var_118)) {
	            *(int8_t *)(rbp + sign_extend_32(var_13C) + 0xfffffffffffffee8) = *(int8_t *)(rbp + sign_extend_32(var_13C) + 0xfffffffffffffee8) & 0xff ^ var_13C + 0x21;
	            var_13C = var_13C + 0x1;
	    }
	    if (strlen(&var_118) == 0x20) {
	            var_138 = 0x69;
	            if (memcmp(&var_138, &var_118, 0x20) == 0x0) {
	                    rax = puts("Correct");
	            }
	            else {
	                    rax = puts(0xa5f);
	            }
	    }
	    else {
	            rax = puts(0xa5f);
	    }
	    rax = 0x0;
	    rcx = *0x28 ^ *0x28;
	    if (rcx != 0x0) {
	            rax = __stack_chk_fail();
	    }
	    else {
	            rbx = stack[2046];
	            rsp = rsp + 0x148;
	            rbp = stack[2047];
	    }
	    return rax;
	}

From the code:

1. We see a string 
2. And then it goes through a for-loop which is: XOR by var_13C (aka. loop index) and then sum of 0x21.

Simple Python scripting to reverse it out

	>>> enc = bytes([0x69, 0x63, 0x77, 0x77, 0x5e, 0x47, 0x44, 0x5c, 0x5c, 0x4b, 0x47, 0x40, 0x54, 0x71, 0x5c, 0x44, 0x58, 0x5e, 0x5f, 0x6b, 0x44, 0x43, 0x5e, 0x4c, 0x5c, 0x65, 0x5e, 0x46, 0x62, 0x52, 0x5e, 0x3d])

	>>> len(enc)
	32

	>>> key = bytes(list(range(len(enc))))
	>>> key
	b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'

	>>> [a^b+0x21 for a,b in zip(enc, key)]
	[72, 65, 84, 83, 123, 97, 99, 116, 117, 97, 108, 108, 121, 95, 115, 116, 105, 108, 108, 95, 113, 117, 105, 116, 101, 95, 101, 122, 95, 108, 97, 125]

	>>> pt = [a^b+0x21 for a,b in zip(enc, key)]

	>>> pt
	[72, 65, 84, 83, 123, 97, 99, 116, 117, 97, 108, 108, 121, 95, 115, 116, 105, 108, 108, 95, 113, 117, 105, 116, 101, 95, 101, 122, 95, 108, 97, 125]

	>>> ''.join(list(map(chr, pt)))
	'HATS{actually_still_quite_ez_la}'

## Flag

	HATS{actually_still_quite_ez_la}
