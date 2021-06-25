import os
from user import create
from database import DataBase

print(f"{DataBase.Count()} Users\n")
print("1- Create users")
print("2- Refresh h_captcha cookie")

r = int(input("Enter number of users ( -1 for unlimited ): "))
tor = input("Enable tor proxy?[y/n]: ").lower()

while (True if r == -1 else False) or (DataBase.Count() <= r):
	print()
	create(True if tor == 'y' else False)

	if tor:
		if os.system("kalitorify -r") != 0:
			print("Failed to stop tor")
		else:
			print("Tor Stopped")