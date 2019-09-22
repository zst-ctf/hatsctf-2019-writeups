import requests

s = requests.session()

res1 = s.get('http://challs.hats.sg:1346/')
captcha = res1.text.split('CAPTCHA: ', 1)[1].split('<', 1)[0]
print(captcha)

data = {
    "submit": captcha,
    "s": "Submit"
}
res2 = s.post('http://challs.hats.sg:1346/', data)
print(res2.text)
