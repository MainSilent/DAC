import os
import sys
from user import create
from database import DataBase
from captcha_token import get_cookie

print(f"{DataBase.Count()} Users\n")
print("1- Create users")
print("2- Refresh h_captcha cookie")

try:
	choice = int(sys.argv[1])
except:
	choice = int(input("Choose by number: "))

if choice == 1:
	#r = int(input("Enter number of users ( -1 for unlimited ): "))
	#tor = input("Enable tor proxy?[y/n]: ").lower()
	tor = 'y'; r = -1

	if tor == 'y':
		if os.system("kalitorify -t") != 0:
			print("Failed to start tor")
		else:
			print("Tor Started")

	while (True if r == -1 else False) or (DataBase.Count() <= r):
		print()
		create(True if tor == 'y' else False)
elif choice == 2:
    get_cookie()