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

        if int(os.getenv("proxy")): 
            options.add_argument('--proxy-server=%s' % Proxy.get())

        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}

        self.driver = webdriver.Chrome(options=options, executable_path="./chromedriver", desired_capabilities=caps)

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

        # Fill out the forms
        print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Webdriver wait")
        WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))

        print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} " +self.email)                          
        self.driver.find_element_by_xpath("//input[@type='email']").send_keys(self.email)

        print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} " +self.username)
        self.driver.find_element_by_xpath("//input[@type='text']").send_keys(self.username)

        print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} " +self.password)
        self.driver.find_element_by_xpath("//input[@type='password']").send_keys(self.password)

        print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL}" +' Random Date')

        self.driver.find_element_by_xpath('//*[@id="react-select-2-input"]').send_keys(str(random.randint(1,12)))
        self.driver.find_element_by_xpath('//*[@id="react-select-2-input"]').send_keys(Keys.ENTER)
        self.driver.find_element_by_xpath('//*[@id="react-select-3-input"]').send_keys(str(random.randint(1,28))) 
        self.driver.find_element_by_xpath('//*[@id="react-select-3-input"]').send_keys(Keys.ENTER)

        random_year = [1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000]

        self.driver.find_element_by_xpath('//*[@id="react-select-4-input"]').send_keys(str(random.choice(random_year)))

        try: 
            self.driver.find_element_by_class_name('inputDefault-3JxKJ2').click() # Agree to terms and conditions
        except:
           ...

        self.driver.find_element_by_class_name('button-3k0cO7').click() # Submit button        
        print(f'{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Submit form')
        
        while True:
            body = self.driver.find_element_by_xpath("/html/body")
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
                            time.sleep(10)
                    except:
                        self.driver.switch_to.parent_frame()
                        break
            time.sleep(0.4)

    def join(self):
        print("Joining the guild...")
        result = f"""
            function getLocalStoragePropertyDescriptor() {{
              const iframe = document.createElement('iframe');
              document.head.append(iframe);
              const pd = Object.getOwnPropertyDescriptor(iframe.contentWindow, 'localStorage');
              iframe.remove();
              return pd;
            }}
            Object.defineProperty(window, 'localStorage', getLocalStoragePropertyDescriptor());
            window.localStorage.heeeeey;
            const localStorage = getLocalStoragePropertyDescriptor().get.call(window);

            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {{
                if (this.readyState == 4)
                    return this.status
            }}
            xhttp.open("POST", "https://discord.com/api/v9/invites/{os.getenv("invite")}", true);
            xhttp.setRequestHeader("authorization", "{token}");
            xhttp.setRequestHeader("x-super-properties", "eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChYMTE7IExpbnV4IHg4Nl82NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzkwLjAuNDQzMC45MyBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiOTAuMC40NDMwLjkzIiwib3NfdmVyc2lvbiI6IiIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjo4NTAzOSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=");
            xhttp.send();
            """

    def send(self):
        ...

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
        print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Error: " + str(e))