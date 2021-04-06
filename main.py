import undetected_chromedriver as uc
uc.install()

import os
import time 
import requests
import random
import string
import sys
import json
import threading
import datetime
import re
from multiprocessing import Process, Manager
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from random_username.generate import generate_username
from colorama import Fore, Style, init 
from bs4 import BeautifulSoup as soup
from sys import stdout
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

init(convert=True)

def password_gen(length=8, chars= string.ascii_letters + string.digits + string.punctuation):
        return ''.join(random.choice(chars) for _ in range(length))  

def free_print(arg):
    print(arg) 

def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response 

class DiscordGen:
    def __init__(self, email, username, password, proxy=None):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}

        self.driver = webdriver.Chrome(options=options, executable_path=r"chromedriver", desired_capabilities=caps)

        self.email= email
        self.username = username
        self.password = password


    def register(self):
        self.driver.get('https://discord.com/register')

        free_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Webdriver wait")
        WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))

        free_print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} " +self.email)                          
        self.driver.find_element_by_xpath("//input[@type='email']").send_keys(self.email)

        free_print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} " +self.username)
        self.driver.find_element_by_xpath("//input[@type='text']").send_keys(self.username)

        free_print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} " +self.password)
        self.driver.find_element_by_xpath("//input[@type='password']").send_keys(self.password)

        free_print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL}" +' Random Date')

        dateWorking = False

        try: #if date could not be found via divs
            self.driver.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/form/div/div[2]/div[4]/div[1]/div[1]/div/div/div/div/div[2]/div').click()
            dateWorking = True
                              
        except:
            free_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} " + 'Error in typing date. Please type the date manually.')
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

            #Submit form
            try: 
                self.driver.find_element_by_class_name('inputDefault-3JxKJ2').click() # Agree to terms and conditions
            except:
                free_print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Could not find button. Ignoring..")
                pass

            self.driver.find_element_by_class_name('button-3k0cO7').click() # Submit button        
            free_print(f'{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Submit form')
            
            return True

    def verify_account(self,link):
        self.driver.get(link)
        free_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Task complete")

    def close_driver(self):
        self.driver.close()

def start_verify(email, email_type):
    free_print(f'{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Checking email inbox.')
    raw_email = email

    if email_type == 'dot':
        email = dfilter_email(raw_email)

    if email_type == 'plus':
        email = pfilter_email(raw_email)

    g = GmailnatorRead(email, raw_email, email_type)

    retry_count = 1

    while retry_count <= 4:
        gmailnator_inbox = g.get_inbox()
        if gmailnator_inbox != '':
            break

        time.sleep(3)
        free_print(f'{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Inbox empty. Retry count: {retry_count}')
        free_print(f'{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Sleeping for 3 seconds. Waiting for Discord email.')
                    
        retry_count += 1

    discord_keywords = re.findall('Discord', gmailnator_inbox)

    if 'Discord' in discord_keywords:
        #retrive messages from inbox
        bs = soup(gmailnator_inbox, 'html.parser')
        href_links = [a['href'] for a in bs.find_all('a')]

        first_message = href_links[0] #get first message which is most likely from Discord verify.

        remove = re.compile('(^.*?(?=[#])[#])') #only get id; remove unnecessary stuff
        first_id = remove.sub('', first_message)
        
        message_html = g.get_single_message(first_id)
        content_html = soup(message_html, 'html.parser')

        message_links = [a['href'] for a in content_html.find_all('a')]

        try:
            discord_verify = message_links[1]
            free_print(f'{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Extracted discord link.')
        except IndexError:
            free_print(f'{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} List index out of range.')
            discord_verify = None

        return discord_verify

    else:
        free_print(f'{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Discord keyword not found. Unable to verify account via email.')
    return False

def get_token(email, password):
    url = "https://discord.com/api/v8/auth/login"

    payload = json.dumps({
      "login": email,
      "password": password,
      "undelete": False,
      "captcha_key": None,
      "login_source": None,
      "gift_code_sku_id": None
    })
    headers = {
      'Content-Type': 'application/json',
      'Cookie': '__cfduid=d1de78589ec090c27e8c088ffc04180be1617519756'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    try:
        return json.loads(response.text)['token']
    except:
        return False

def worker(count):
    print("\033[33m"+"\nCreated: "+str(count.value)+"\n\033[0m")
    # free_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Scraping email. ")

    # g = GmailnatorGet()
    # new_email = g.get_email()
    
    # free_print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Scraped {new_email}")
 
    # email_type = find_email_type(new_email)

    # if email_type =='dot':
    #     filtered_email = dfilter_email(new_email)

    # if email_type == 'plus':
    #     filtered_email = pfilter_email(new_email)

    username = generate_username(1)[0]
    new_email = username + "@gmail.com"
    password = password_gen()    

    d = DiscordGen(new_email, username, password)

    try:
        d.register() 

        # try:
        #     verify_link = start_verify(new_email, email_type)
        #     if verify_link:
        #         d.verify_account(verify_link)
        #         d.close_driver()

        #     else:
        #         d.verify_account('https://www.gmailnator.com/inbox/#' + new_email)

        # except Exception as e:
        #     print('some error occured')
        #     print(e)
        #     d.verify_account('https://www.gmailnator.com/inbox/#' + new_email)
        #     d.close_driver()   
                     
    except Exception as e:
        free_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Webdriver Error: " + str(e))

    time.sleep(55)
    token = get_token(new_email, password)

    if token:
        with open('.env', 'a', encoding='UTF-8') as f:
            f.write(token+'\n') 
        count.value += 1
        print("\033[32m"+"Account created\n"+"\033[0m")
    else:
        print("\033[31m"+"Failed to get token\n"+"\033[0m")
          
# -------------------------- Main -----------------------------

from database import DataBase, G_DataBase
from channel import fetch

print(f"{DataBase.nCount()}/{DataBase.Count()} Users\n")
print("1- Get guilds")
print("2- Fetch users from guilds")
print("3- Send message to users")
print("4- Reset sent data")
print("5- Truncate users")

choice = int(input("Choose by number: "))

if choice == 1:
    guild()
elif choice == 2:
    fetch()
elif choice == 3:
    lst = DataBase.GetFromDB()
    for users in [lst[i:i + 4] for i in range(0, len(lst), 4)]:
        print("\033[33m"+"Changing token..."+"\033[0m")
        change_token()

        for user in users:
            message = User(user[2])

            if not int(user[3]) and message.create() and message.send():
                DataBase.SendUpdate(user[2])
                print(f"Sending to {user[1]} "+"\033[32m"+"Success"+"\033[0m")
            elif not int(user[3]):
                print(f"Sending to {user[1]} "+"\033[31m"+"Failed"+"\033[0m")
elif choice == 4:
    print("Reseting...")
    DataBase.Reset()
elif choice == 5:
    print("Truncating...")
    DataBase.truncate()

# manager = Manager()
# count = manager.Value('count', 0)

# while True:
#     p = Process(target=worker, args=(count,))
#     p.start()
#     time.sleep(110)
#     p.terminate()
#     os.system("pkill chromium; pkill chrome")
#     print("Waiting for next worker...")
#     time.sleep(110)