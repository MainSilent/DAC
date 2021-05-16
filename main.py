import os
import time 
from multiprocessing import Process, Manager
from hcaptcha import get_cookie
from database import DataBase, Proxy
from client import worker
from channel import fetch
from dotenv import load_dotenv; load_dotenv()

print(f"{Proxy.count()} Proxy")
print(f"{DataBase.sentCount()} Users sent\n")
print("1- Send message to users")
print("2- Fetch users")
print("3- Add proxy")
print("4- Refresh h_captcha cookie")
print("5- Truncate sent")

manager = Manager()
scroll = manager.Value('scroll', 0)
choice = int(input("Choose by number: "))

if choice == 1:
	max_range = int(input("max range: "))
	while True:
		if max_range != -1 and DataBase.sentCount() >= max_range:
			break
			print("Max messages reached")

		p = Process(target=worker, args=(scroll,))
		p.start()
		time.sleep(110)
		p.terminate()
		os.system("pkill chromium; pkill chrome")
		if max_range != -1:
			print(f"{DataBase.sentCount()}/{max_range} sent")
		else:
			print(f"{DataBase.sentCount()} sent")

		if not int(os.getenv("proxy")) and max_range == -1 or not DataBase.sentCount() >= max_range:
			print("Waiting for next worker...\n")
			time.sleep(110)
elif choice == 2:
	fetch()
elif choice == 3:
	print()
	while True:
		addr = input("Address: ")
		if addr.lower() == "q":
			break
		Proxy.add(addr)
elif choice == 4:
    get_cookie()
elif choice == 5:
    print("Truncating...")
    DataBase.truncate()