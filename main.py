import os
import time 
from multiprocessing import Process
from hcaptcha import get_cookie
from database import DataBase, Proxy
from client import worker

print(f"{Proxy.count()} Proxy")
print(f"{DataBase.sentCount()} Users sent\n")
print("1- Send message to users")
print("2- Add proxy")
print("3- Refresh h_captcha cookie")
print("4- Truncate users")

choice = int(input("Choose by number: "))

if choice == 1:
	worker()
elif choice == 2:
	print()
	while True:
		addr = input("Address: ")
		if addr.lower() == "q":
			break
		Proxy.add(addr)
elif choice == 3:
    get_cookie()
elif choice == 4:
    print("Truncating...")
    DataBase.truncate()