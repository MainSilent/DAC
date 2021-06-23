from user import create
from database import DataBase
from captcha_token import get_cookie

print(f"{DataBase.Count()} Users\n")
print("1- Create users")
print("2- Refresh h_captcha cookie")

choice = int(input("Choose by number: "))

if choice == 1:
	create()
elif choice == 2:
    get_cookie()