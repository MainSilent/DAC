import os
from user import create
from database import DataBase
from captcha_token import get_cookie

print(f"{DataBase.Count()} Users\n")
print("1- Create users")
print("2- Refresh h_captcha cookie")

choice = int(input("Choose by number: "))

if choice == 1:
	r = int(input("Enter number of users ( -1 for unlimited ): "))
	tor = input("Enable tor proxy?[y/n]: ").lower()

	while (True if r == -1 else False) or (DataBase.Count() <= r):
		print()

		if tor == 'y':
			if os.system("") != 0:
				print("Failed to start tor")
			else:
				print("Tor Started")

		create()

		if tor == 'y':
			if os.system("") != 0:
				print("Failed to stop tor")
			else:
				print("Tor Stopped")
elif choice == 2:
    get_cookie()