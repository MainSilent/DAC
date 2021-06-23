import json
import requests
from random_username.generate import generate_username

headers = {
  'X-Track': 'eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChYMTE7IExpbnV4IHg4Nl82NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzkxLjAuNDQ3Mi43NyBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiOTEuMC40NDcyLjc3Iiwib3NfdmVyc2lvbiI6IiIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjo5OTk5LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
  'Content-Type': 'application/json',
  'Cookie': '__dcfduid=61f8ced90af24ebc9736ccf74c566850'
}

register_url = "https://discord.com/api/v9/auth/register"
settings_url = "https://discord.com/api/v9/users/@me/settings"

def is_valid(token):
	response = requests.request("GET", settings_url, headers={'authorization': token})
	if response.status_code == 200:
		print(token)
		return True
	else:
		print("Busted!")
		return False

def create():
	payload = json.dumps({
		"consent": True,
		"username": generate_username(1)[0],
		"captcha_key": ""
	})
	response = requests.request("POST", register_url, headers=headers, data=payload)
	try:
		is_valid(json.loads(response.text)["token"])
	except:
		print(response.text)
		print("Failed")