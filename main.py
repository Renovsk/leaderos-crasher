import requests
import threading
import re
import string, random

url = "https://www.website.com"
endpoint = "/register/"

def getcsrf():
    r = requests.get(url + endpoint)
    csrf_matches = re.findall(r'<input type="hidden" name="csrf_token" value="(.*?)">', r.text)
    php = r.cookies.get_dict().get('PHPSESSID')
    if csrf_matches and php:
        print(f"received {csrf_matches[0]} && {php}")
        return csrf_matches[0], php
    return None, None

def main():
    print('fetching csrf')
    csrf, php = getcsrf()
    if not csrf or not php:
        print("is the website down?")
        return

    username = "".join(random.choices(string.ascii_letters, k=12))
    email = f"{username}@gmail.com"
    password = "".join(random.choices(string.ascii_letters + string.digits, k=19))
    print(f'generated password {password}')

    headers = {
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": "\"Chromium\";v=\"135\", \"Not-A.Brand\";v=\"8\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Linux\"",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": url,
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": url + endpoint,
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=0, i"
    }

    data = {
        "csrf_token": csrf,
        "username": username,
        "email": email,
        "password": password,
        "passwordRe": password
    }

    cookies = {
        "CSRF-TOKEN": csrf,
        "PHPSESSID": php
    }

    r = requests.post(url + endpoint, headers=headers, data=data, cookies=cookies)

    if r.status_code == 200:
        print(f"made account | email: {email} | username: {username} | password: {password}")

    else:
        print(f"status: {r.status_code}")

threads = []
if __name__ == '__main__':
    while True:
        for i in range(70): # amount of threading here 😛😛😛
            t = threading.Thread(target=main)
            t.start()
            threads.append(t)
