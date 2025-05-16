import random
import string
import requests
import hashlib
from faker import Faker

print(f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓           
> › Github :- @vraxyxx 
> › By      :- https://www.facebook.com/revn.19
> › Proxy Support Hardcoded by @coopers-lab
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛                
""")
print('\x1b[38;5;208m⇼'*60)

# ✅ Hardcoded proxy
proxy = {
    "http": "http://124.104.137.71:8080",
    "https": "http://124.104.137.71:8080"
}

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_mail_domains():
    try:
        r = requests.get("https://api.mail.tm/domains", proxies=proxy, timeout=10)
        if r.status_code == 200:
            return r.json()['hydra:member']
        else:
            print("[×] Error fetching mail domains.")
    except Exception as e:
        print(f"[×] Domain Fetch Error: {e}")
    return []

def create_email_account():
    fake = Faker()
    domains = get_mail_domains()
    if not domains:
        return None, None, None, None, None

    domain = random.choice(domains)['domain']
    username = generate_random_string(10)
    password = fake.password()
    address = f"{username}@{domain}"
    birthday = fake.date_of_birth(minimum_age=18, maximum_age=45)
    first_name = fake.first_name()
    last_name = fake.last_name()

    data = {"address": address, "password": password}
    headers = {"Content-Type": "application/json"}

    try:
        r = requests.post("https://api.mail.tm/accounts", json=data, headers=headers, proxies=proxy, timeout=10)
        if r.status_code == 201:
            return address, password, first_name, last_name, birthday
        else:
            print("[×] Failed to create mail account:", r.text)
    except Exception as e:
        print(f"[×] Email Account Error: {e}")
    return None, None, None, None, None

def fb_register(email, password, first_name, last_name, birthday):
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

    # Facebook signature
    sig_string = ''.join(f"{k}={v}" for k, v in sorted(req.items()))
    req['sig'] = hashlib.md5((sig_string + secret).encode()).hexdigest()

    headers = {
        'User-Agent': '[FBAN/FB4A;FBAV/35.0.0.48.273;FBDM/{density=1.33125,width=800,height=1205};FBLC/en_US;FBCR/;FBPN/com.facebook.katana;FBDV/Nexus 7;FBSV/4.1.1;FBBK/0;]'
    }

    try:
        r = requests.post("https://b-api.facebook.com/method/user.register", data=req, headers=headers, proxies=proxy, timeout=10)
        result = r.json()
        if 'new_user_id' in result:
            print(f"""
-----------ACCOUNT CREATED-----------
EMAIL    : {email}
PASSWORD : {password}
NAME     : {first_name} {last_name}
BIRTHDAY : {birthday}
GENDER   : {gender}
USER ID  : {result['new_user_id']}
TOKEN    : {result.get('session_info', {}).get('access_token', 'N/A')}
-------------------------------------
""")
        else:
            print("[×] Facebook registration failed:", result)
    except Exception as e:
        print(f"[×] Facebook Error: {e}")

# Main
try:
    count = int(input("[+] How Many Accounts You Want To Create? "))
    for _ in range(count):
        email, pwd, fname, lname, dob = create_email_account()
        if email:
            fb_register(email, pwd, fname, lname, dob)
        else:
            print("[×] Skipped due to email creation error.")
except Exception as e:
    print(f"[×] Error: {e}")
