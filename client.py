import undetected_chromedriver as uc
uc.install()

import os
import time
import json 
import random
import string
from database import DataBase, Proxy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from random_username.generate import generate_username
from colorama import Fore, Style
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from dotenv import load_dotenv; load_dotenv()

last_scroll = 0
filter_status = int(os.getenv("filter")) 
default_avatars = [
    "322c936a8c8be1b803cd94861bdfa868", # Gray
    "6debd47ed13483642cf09e832ed0bc1b", # Blue
    "1cbd08c76f8af6dddce02c5138971129", # Red
    "dd4dbc0016779df1378e7812eabaa04d", # Green
    "0e291f67c9274a1abdddeb3fd919cbaa", # Yellow
]

def password_gen(length=8, chars= string.ascii_letters + string.digits + string.punctuation):
        return ''.join(random.choice(chars) for _ in range(length))  

class DiscordGen:
    def __init__(self, email, username, password):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        #options.add_argument('--proxy-server=%s' % Proxy.get())

        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}

        self.driver = webdriver.Chrome(options=options, executable_path=r"chromedriver", desired_capabilities=caps)

        self.email= email
        self.username = username
        self.password = password

    def register(self):
        self.driver.get('http://www.example.com')

        try:
            with open("h_captcha.json", "r") as f:
                h_captcha = json.load(f)
            for cookie in h_captcha:
                self.driver.add_cookie(cookie)
        except Exception as e:
            print(e)

        self.driver.get('https://discord.com/register')

        print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Webdriver wait")
        WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))

        print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} " +self.email)                          
        self.driver.find_element_by_xpath("//input[@type='email']").send_keys(self.email)

        print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} " +self.username)
        self.driver.find_element_by_xpath("//input[@type='text']").send_keys(self.username)

        print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} " +self.password)
        self.driver.find_element_by_xpath("//input[@type='password']").send_keys(self.password)

        print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL}" +' Random Date')

        dateWorking = False

        try: #if date could not be found via divs
            self.driver.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/form/div/div[2]/div[4]/div[1]/div[1]/div/div/div/div/div[2]/div').click()
            dateWorking = True
                              
        except:
            print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} " + 'Error in typing date. Please type the date manually.')
            input(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Submit your form manually. Have you solved captcha? [y/n] > ")
            dateWorking = False

        if dateWorking:
            actions = ActionChains(self.driver)

            actions.send_keys(str(random.randint(1,12)))# Month
            actions.send_keys(Keys.ENTER)
            actions.send_keys(str(random.randint(1,28))) #Day
            actions.send_keys(Keys.ENTER)

            random_year = [1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000]

            actions.send_keys(str(random.choice(random_year))) #Year
            actions.perform()

            try: 
                self.driver.find_element_by_class_name('inputDefault-3JxKJ2').click() # Agree to terms and conditions
            except:
               ...

            self.driver.find_element_by_class_name('button-3k0cO7').click() # Submit button        
            print(f'{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Submit form')
            
            body = self.driver.find_element_by_xpath("/html/body")

            while True:
                if "https://discord.com/channels/@me" == self.driver.current_url and body.text and "DID YOU KNOW" not in body.text:
                    if "Join a server" in body.text:
                        newData = DataBase('', self.username, 0)
                        newData.GoToDB()
                        return True
                    else:
                        self.close_driver()
                        return False
                elif "Email is already registered" in body.text:
                    self.close_driver()
                    worker()
                elif "checkbox" in body.get_attribute('innerHTML') and "Beep" in body.text:
                    self.driver.switch_to.frame(0)
                    while True:
                        try:
                            if not self.driver.find_element_by_id("checkbox").get_attribute("style"):
                                self.driver.find_element_by_id("checkbox").send_keys(Keys.ENTER)
                        except:
                            self.driver.switch_to.parent_frame()
                            break

                time.sleep(0.4)

    def join(self):
        print("Joining the guild...")
        self.driver.execute_script('document.querySelector("a .joinCTA-1s7TZx").click()')
        self.driver.find_element_by_class_name("input-cIJ7To").send_keys(os.getenv("invite"))
        self.driver.execute_script('document.querySelector(".justifyBetween-2tTqYu .button-38aScr").click()')
        
        if "https://discord.com/channels/@me" != self.driver.current_url:
            self.close_driver()
            return False

        while True:
            if "https://discord.com/channels/@me" != self.driver.current_url:
                break
            elif "The invite is invalid or has expired." in self.driver.find_element_by_xpath("/html/body").text:
                print("\033[31m"+"Invalid invite code!"+"\033[0m")
                raise Exception("invalid invite")

        return True

    def send(self, count = 0):
        while True:
            try:
                if self.driver.find_element_by_class_name('member-3-YXUe').text:
                    break
            except:
                time.sleep(0.4)

        users = self.driver.find_elements_by_class_name('member-3-YXUe')
        if self.check(users):
            for user in users:
                if count < 4:
                    name = user.find_element_by_class_name('name-uJV0GL').text
                    if not DataBase.Status(name) and name != self.username and not len(user.find_elements_by_class_name("botText-1526X_")):
                        if filter_status and self.check_profile(user):
                            continue
                        user.click()
                        self.driver.find_elements_by_class_name("input-cIJ7To")[1].send_keys(os.getenv("msg"))
                        self.driver.find_elements_by_class_name("input-cIJ7To")[1].send_keys(Keys.ENTER)
                        
                        body = self.driver.find_element_by_xpath("/html/body")

                        while True:
                            if name in body.text and os.getenv("msg") in body.text or "Something's Going on Here" in body.text:
                                break
                            time.sleep(0.4)
                        if filter_status:
                            time.sleep(2)

                        if "Clyde" in body.text and "Your message could not be delivered." in body.text:
                            print(f"Sending to {name} "+"\033[31m"+"Failed"+"\033[0m"+", user doesn't allow direct message")
                            newData = DataBase('', name, 1)
                            newData.GoToDB()
                        elif "Something's Going on Here" in body.text:
                            print(f"Sending to {name} "+"\033[31m"+"Failed"+"\033[0m"+", system detected!")
                            self.close_driver()
                            return False
                        else:
                            print(f"Sending to {name} "+"\033[32m"+"Success"+"\033[0m")
                            newData = DataBase('', name, 2)
                            newData.GoToDB()

                        count += 1
                        self.driver.back()
                        self.send(count)

                # Leave the guild
                else:
                    self.driver.find_element_by_class_name("header-2V-4Sw").click()
                    time.sleep(1)
                    self.driver.find_element_by_class_name("colorDanger-2qLCe1").click()

                    while True:
                        if len(self.driver.find_elements_by_class_name("colorRed-1TFJan")):
                            break
                        time.sleep(0.4)
                    self.driver.find_element_by_class_name("colorRed-1TFJan").click()

                    while True:
                        if not len(self.driver.find_elements_by_class_name("colorRed-1TFJan")):
                            break
                        time.sleep(0.4)
                    if len(self.driver.find_elements_by_class_name("childWrapper-anI2G9")) == 1:
                        print("\033[32m"+"Leaved the guild successfully"+"\033[0m")
                    else:
                        print("\033[31m"+"Leaving the guild failed!"+"\033[0m")
                        with open("failed.txt", "a") as f:
                            f.write(f'{self.username}\n{self.password}\n\n')

                    break
        # scroll if check failed
        else:
            if count == 4:
                return True

            global last_scroll
            self.driver.execute_script(f'document.querySelector(".members-1998pB").scroll(0, {last_scroll})')
            users = self.driver.find_elements_by_class_name('member-3-YXUe')
            
            while not self.check(users):
                last_scroll += 100
                self.driver.execute_script(f'document.querySelector(".members-1998pB").scroll(0, {last_scroll})')
                users = self.driver.find_elements_by_class_name('member-3-YXUe')
            self.send(count)

        return True

    def check(self, users):
        try:
            res = []
            for user in users:
                name = user.find_element_by_class_name('name-uJV0GL').text
                if not DataBase.Status(name) and name != self.username and not len(user.find_elements_by_class_name("botText-1526X_")):
                    if filter_status and self.check_profile(user):
                        continue
                    res.append(user)

            return len(res)
        except:
            return False

    def check_profile(self, user):
        url = user.find_element_by_class_name("avatar-VxgULZ").get_attribute("src")
        url = url.split("/")[-1].split(".")[0]
        if url in default_avatars:
            return True
        return False

    def close_driver(self):
        self.driver.close()

def worker():
    username = generate_username(1)[0]
    new_email = username + "@gmail.com"
    password = password_gen()    

    d = DiscordGen(new_email, username, password)

    try:
        if d.register():
            print("\033[32m"+"Account created successfully"+"\033[0m")
        else:
            print("\033[31m"+"Registration failed, system detected!"+"\033[0m")
            return

        if d.join():
            print("\033[32m"+"Joined the guild successfully"+"\033[0m")
        else:
            print("\033[31m"+"Joining the guild failed!"+"\033[0m")
            return
        
        if not d.send():
            return
        
    except Exception as e:
        ...
        #print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Webdriver Error: " + str(e))