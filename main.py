import os
from hcaptcha import get_cookie
from database import DataBase
from client import worker
from channel import fetch

print(f"{DataBase.sentCount()}/{DataBase.nCount()} Users sent\n")
print("1- Send message to users")
print("2- Fetch users")
print("3- Add proxy")
print("4- Refresh h_captcha cookie")

choice = int(input("Choose by number: "))

if choice == 1:
	max_range = int(input("max range: "))
	while True:
		if max_range != -1 and DataBase.sentCount() >= max_range:
			break
			print("Max messages reached")

		p = Process(target=worker)
		p.start()
		time.sleep(1210)
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