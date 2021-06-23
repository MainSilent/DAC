from user import create
from database import DataBase
from captcha_token import get_cookie

print(f"{DataBase.Count()} Users\n")
print("1- Create users")
print("2- Refresh h_captcha cookie")

choice = int(input("Choose by number: "))

if choice == 1:
	r = int(input("Enter number of users ( -1 for unlimited ): "))
	while (True if r == -1) or (DataBase.Count() <= r):
		print()
		create()
elif choice == 2:
    get_cookie()