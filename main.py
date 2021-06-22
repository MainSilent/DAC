from database import DataBase

print(f"{DataBase.Count()} Users\n")
print("1- Create users")
print("2- Refresh h_captcha cookie")

choice = int(input("Choose by number: "))

if choice == 1:
	...
elif choice == 2:
    get_cookie()