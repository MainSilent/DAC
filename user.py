import os
import json
import string
import random
import hcaptcha
import requests
from database import DataBase
from dotenv import load_dotenv; load_dotenv()
from random_username.generate import generate_username

invite = os.getenv("invite")
register_url = "https://discord.com/api/v9/auth/register"
settings_url = "https://discord.com/api/v9/users/@me/settings"

def password_gen(length=8, chars= string.ascii_letters + string.digits + string.punctuation):
        return ''.join(random.choice(chars) for _ in range(length))  

def is_valid(token):
	response = requests.request("GET", settings_url, headers={'authorization': token})
	if response.status_code == 200:
		print(token)
		return True
	else:
		print("Token is banned")
		return False

def join(token):
    try:
        url = "https://discord.com/api/v8/invites/" + invite
        headers = {
            'Cookie': '__cfduid=db07e6c454c1cb90e3b903a6500527f391617469496',
            'authorization': token,
            'x-super-properties': 'eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChYMTE7IExpbnV4IHg4Nl82NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg5LjAuNDM4OS45MCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiODkuMC40Mzg5LjkwIiwib3NfdmVyc2lvbiI6IiIsInJlZmVycmVyIjoiaHR0cHM6Ly9kaXNjb3JkLmNvbS8iLCJyZWZlcnJpbmdfZG9tYWluIjoiZGlzY29yZC5jb20iLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODEzMjksImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers)
        if response.status_code == 200:
            print("Joined")
            return True
        else:
            print("Failed to Join")
            return False
    except:
        print("\033[31m"+"Failed to join the guild"+"\033[0m")
        return False

def create():
	try:
		response = None
		user = generate_username(1)[0]
		print("Getting new key...")
		captcha_key = hcaptcha.new()
		if not captcha_key:
			raise Exception("Failed to get captcha key")
		print("\033[33mSuccessfully received captcha key\033[0m")

		# For now we only want to invite, for not getting accounts ban uncomment the headers
		headers = {
			'Content-Type': 'application/json',
			'Cookie': '__dcfduid=61f8ced90af24ebc9736ccf74c566850',
			'X-Track': 'eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChYMTE7IExpbnV4IHg4Nl82NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzkxLjAuNDQ3Mi43NyBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiOTEuMC40NDcyLjc3Iiwib3NfdmVyc2lvbiI6IiIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjo5OTk5LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=='
		}
		payload = json.dumps({
			"username": user,
			"email": f"{user}{password_gen(10, string.digits)}@gmail.com",
			"password": password_gen(),
			"date_of_birth": "1998-05-14",
			"consent": True,
			"invite": invite if invite else None,
			"gift_code_sku_id": None,
			"captcha_key": captcha_key
		})
		print("Sending register...")
		response = requests.request("POST", register_url, headers=headers, data=payload)
		token = json.loads(response.text)["token"]
		is_valid(token)
		if token:
			newUser = DataBase(token, user)
			newUser.GoToDB()
			print(f"Creating {user}, \033[32mSuccess\033[0m - {DataBase.Count()}")
		else:
			raise Exception("failed to get token")
	except Exception as e:
		try:
			print(response.text)
		except:
			print(e)
		print(f"Creating {user}, \033[31mFailed\033[0m - {DataBase.Count()}")