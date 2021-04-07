import os
import time 
from multiprocessing import Process
from database import DataBase
from client import worker

print("\n1- Send message to users")
print("2- Truncate users")

choice = int(input("Choose by number: "))

if choice == 1:
	worker()
elif choice == 2:
    print("Truncating...")
    DataBase.truncate()