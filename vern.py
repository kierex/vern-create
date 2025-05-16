import threading
from queue import Queue
import requests
import random
import string
import json
import hashlib
from faker import Faker

print(f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓           
> › Github :- @vraxyxx 
> › By      :- https://www.facebook.com/revn.19
> › Proxy Support Added by @coopers-lab
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
""")
print('\x1b[38;5;208m⇼' * 60)
print('\x1b[38;5;22m•' * 60)
print('\x1b[38;5;22m•' * 60)
print('\x1b[38;5;208m⇼' * 60)

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_mail_domains(proxy=None):
    try:
        response = requests.get("https://api.mail.tm/domains", proxies=proxy, timeout=10)
        if response.status_code == 200:
            return response.json().get('hydra:member', [])
        print(f'[×] E-mail Error : {response.text}')
    except Exception as e:
        print(f'[×] Error fetching domains: {e}')
    return None

def create_mail_tm_account(proxy=None):
    fake = Faker()
    mail_domains = get_mail_domains(proxy)
    if not mail_domains:
        return None, None, None, None, None

    domain = random.choice(mail_domains).get('domain')
    username = generate_random_string(10)
    password = fake.password()
    birthday = fake.date_of_birth(minimum_age=18, maximum_age=45)
    first_name = fake.first_name()
    last_name = fake.last_name()

    url = "https://api.mail.tm/accounts"
    headers = {"Content-Type": "application/json"}
    data = {"address": f"{username}@{domain}", "password": password}

    try:
        response = requests.post(url, headers=headers, json=data, proxies=proxy, timeout=10)
        if response.status_code == 201:
            return f"{username}@{domain}", password, first_name, last_name, birthday
        else:
            print(f'[×] Email Creation Error : {response.text}')
    except Exception as e:
        print(f'[×] Exception during email creation: {e}')
    return None, None, None, None, None

def _call(url, params, proxy=None, post=True):
    headers = {
        'User-Agent': '[FBAN/FB4A;FBAV/35.0.0.48.273;FBDM/{density=1.33125,width=800,height=1205};FBLC/en_US;FBCR/;FBPN/com.facebook.katana;FBDV/Nexus 7;FBSV/4.1.1;FBBK/0;]'
    }
    try:
        if post:
            response = requests.post(url, data=params, headers=headers, proxies=proxy, timeout=10)
        else:
            response = requests.get(url, params=params, headers=headers, proxies=proxy, timeout=10)
        return response.json()
    except Exception as e:
        print(f'[×] API Call Error: {e}')
        return {}

def register_facebook_account(email, password, first_name, last_name, birthday, proxy=None):
    api_key = '882a8490361da98702bf97a021ddc14d'
    secret = '62f8ce9f74b12f84c123cc23437a4a32'
    gender = random.choice(['M', 'F'])

    req = {
        'api_key': api_key,
        'attempt_login': True,
        'birthday': birthday.strftime('%Y-%m-%d'),
        'client_country_code': 'EN',
        'fb_api_caller_class': 'com.facebook.registration.protocol.RegisterAccountMethod',
        'fb_api_req_friendly_name': 'registerAccount',
        'firstname': first_name,
        'format': 'json',
        'gender': gender,
        'lastname': last_name,
        'email': email,
        'locale': 'en_US',
        'method': 'user.register',
        'password': password,
        'reg_instance': generate_random_string(32),
        'return_multiple_errors': True
    }

    sorted_req = sorted(req.items())
    sig = ''.join(f'{k}={v}' for k, v in sorted_req)
    req['sig'] = hashlib.md5((sig + secret).encode()).hexdigest()

    reg = _call('https://b-api.facebook.com/method/user.register', req, proxy)

    if 'new_user_id' in reg and 'session_info' in reg:
        user_id = reg['new_user_id']
        token = reg['session_info'].get('access_token', 'N/A')

        print(f'''
-----------GENERATED-----------
EMAIL : {email}
ID : {user_id}
PASSWORD : {password}
NAME : {first_name} {last_name}
BIRTHDAY : {birthday} 
GENDER : {gender}
-----------GENERATED-----------
Token : {token}
-----------GENERATED-----------''')

        with open('username.txt', 'a') as file:
            file.write(f'{email} | {password} | {first_name} {last_name} | {birthday} | {gender} | {user_id} | {token}\n')
    else:
        print('[×] Failed to register account. Response:', reg)

def test_proxy(proxy, q, valid_proxies):
    if test_proxy_helper(proxy):
        valid_proxies.append(proxy)
    q.task_done()

def test_proxy_helper(proxy):
    try:
        response = requests.get('https://api.mail.tm', proxies=proxy, timeout=5)
        print(f'Pass: {proxy}')
        return response.status_code == 200
    except:
        print(f'Fail: {proxy}')
        return False

def load_proxies():
    try:
        with open('proxies.txt', 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        return [{'http': f'http://{proxy}', 'https': f'http://{proxy}'} for proxy in proxies]
    except FileNotFoundError:
        print('[×] proxies.txt not found.')
        return []

def get_working_proxies():
    proxies = load_proxies()
    valid_proxies = []
    q = Queue()
    for proxy in proxies:
        q.put(proxy)

    for _ in range(10):  # 10 threads
        worker = threading.Thread(target=worker_test_proxy, args=(q, valid_proxies))
        worker.daemon = True
        worker.start()

    q.join()
    return valid_proxies

def worker_test_proxy(q, valid_proxies):
    while True:
        proxy = q.get()
        if proxy is None:
            break
        test_proxy(proxy, q, valid_proxies)

# MAIN EXECUTION
working_proxies = get_working_proxies()

if not working_proxies:
    print('[×] No working proxies found. Please check your proxies.')
else:
    try:
        num_accounts = int(input('[+] How Many Accounts You Want:  '))
        for _ in range(num_accounts):
            proxy = random.choice(working_proxies)
            email, password, first_name, last_name, birthday = create_mail_tm_account(proxy)
            if all([email, password, first_name, last_name, birthday]):
                register_facebook_account(email, password, first_name, last_name, birthday, proxy)
            else:
                print('[×] Failed to create mail account, skipping...')
    except ValueError:
        print('[×] Invalid input. Please enter a number.')

print('\x1b[38;5;208m⇼' * 60)
