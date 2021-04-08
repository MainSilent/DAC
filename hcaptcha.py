import undetected_chromedriver as uc
uc.install()

import os
import time
import json
from selenium import webdriver
from dotenv import load_dotenv; load_dotenv()

def get_cookie():
	print("Waiting for hcaptcha cookie...")
	driver = webdriver.Chrome(executable_path="chromedriver")
	driver.get("https://accounts.hcaptcha.com/verify_email/"+os.getenv("hcaptcha"))
	while True:
		if "Set Cookie" in driver.find_element_by_xpath("/html/body").text:
			break
		time.sleep(0.4)
	time.sleep(2)
	driver.find_element_by_class_name("sc-cSHVUG").click()

	while True:
		try:
			res = driver.find_element_by_class_name("dcPVkS").text
			if "Cookie set" in res:
				with open("h_captcha.json", "w") as f:
				    f.write(json.dumps(driver.get_cookies()))
				print("\033[32m"+"Success"+"\033[0m")
				break 
			else:
				print("\033[31m"+"Failed"+"\033[0m"+", "+res)
				break
		except:
			time.sleep(0.4)