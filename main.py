from database import DataBase

print(f"{DataBase.sentCount()}/{DataBase.nCount()} Users sent\n")
print("1- Create users")
print("2- Refresh h_captcha cookie")

choice = int(input("Choose by number: "))

if choice == 1:
	...
elif choice == 2:
    get_cookie()