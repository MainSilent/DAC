import os
from user import create
from database import DataBase
from multiprocessing import Process

print(f"{DataBase.Count()} Users\n")

r = int(input("Enter number of users ( -1 for unlimited ): "))
tor = input("Enable tor proxy?[y/n]: ").lower()

while (True if r == -1 else False) or (DataBase.Count() <= r):
	print()
	p = Process(target=create)
	p.start()
	p.join()

	if tor == 'y':
		if os.system("kalitorify -r > /dev/null") != 0:
			print("\033[31mFailed to restart tor\033[0m")
		else:
			print("\033[32mTor restarted\033[0m")