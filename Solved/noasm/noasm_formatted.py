(lambda __print, __g, __y: [
  [
    [
      [
        [(lambda __after: (sys.stdout.write('Tell me the flag and I will let you know if you are right: '), [(lambda __after: (__print('WRONG'), (exit(0), __after())[1])[1]
            if (len(pw) != 19)
            else __after())(lambda: [(lambda __after: (__print('WRONG1'), (exit(0), __after())[1])[1]
            if (int(('0x' + p), 0) != 310333690747)
            else __after())(lambda: [(lambda __after: (__print('WRONG2'), (exit(0), __after())[1])[1]
            if (b != ''.join(map(chr, [89, 88, 78, 116, 88, 119, 61, 61])))
            else __after())(lambda: [(lambda __after: (__print('WRONG3'), (exit(0), __after())[1])[1]
            if (h != '109dd7decb2e3a3658db75dcad688658')
            else __after())(lambda: [(lambda __items, __after, __sentinel: __y(lambda __this: lambda: (lambda __i: [
              [(random.seed(c), (lambda __after: (__print('WRONG4'), (exit(0), __after())[1])[1]
                  if (r != random.randint(0, 100))
                  else __after())(lambda: __this()))[1]
                for __g['c'] in [(pw[i])]
              ][0]
              for (__g['i'], __g['r']) in [(__i)]
            ][0]
            if __i is not __sentinel
            else __after())(next(__items, __sentinel)))())(iter(zip(range(13, 19), rs)), lambda: (__print("That's the flag, go submit it."), __after())[1], [])
             for __g['rs'] in [([87, 16, 33, 1, 56, 73])]][0])
            for __g['h'] in [(hashlib.md5(pw[9: 13]).hexdigest())]][0])
            for __g['b'] in [(base64.b64encode(pw[5: 9]))]][0])
            for __g['p'] in [(binascii.hexlify(pw[0: 5]))]][0])
            for __g['pw'] in [(raw_input())]][0])[1]
          if (__name__ == '__main__')
          else __after())(lambda: None) for __g['random'] in [(__import__('random', __g, __g))]][0]
        for __g['hashlib'] in [(__import__('hashlib', __g, __g))]
      ][0]
      for __g['sys'] in [(__import__('sys', __g, __g))]
    ][0]
    for __g['base64'] in [(__import__('base64', __g, __g))]
  ][0]
  for __g['binascii'] in [(__import__('binascii', __g, __g))]
][0])(__import__('__builtin__', level = 0).__dict__['print'], globals(), (lambda f: (lambda x: x(x))(lambda y: f(lambda: y(y)()))))