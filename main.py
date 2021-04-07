import time 
from multiprocessing import Process
from database import DataBase
from client import worker
from channel import fetch

print(f"{DataBase.nCount()}/{DataBase.Count()} Users\n")
print("1- Fetch users from guilds")
print("2- Send message to users")
print("3- Reset sent data")
print("4- Truncate users")

choice = int(input("Choose by number: "))

if choice == 1:
    fetch()
elif choice == 2:
    lst = DataBase.GetFromDB()
    for users in [lst[i:i + 4] for i in range(0, len(lst), 4)]:
	    p = Process(target=worker, args=(users,))
	    p.start()
	    time.sleep(110)
	    p.terminate()
	    os.system("pkill chromium; pkill chrome")
	    print("Waiting for next worker...")
	    time.sleep(110)
elif choice == 3:
    print("Reseting...")
    DataBase.Reset()
elif choice == 4:
    print("Truncating...")
    DataBase.truncate()