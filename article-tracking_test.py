#!/usr/local/bin/python3.6




# article-tracking_test.py
# Using the "requests" package for sending
# Telegram messages and Heroku to have a permanent solution: a server




## Setting the current working directory automatically
# import os
# project_path = os.getcwd() # getting the path leading to the current working directory
# os.getcwd() # printing the path leading to the current working directory
# os.chdir(project_path) # setting the current working directory based on the path leading to the current working directory




## Required packages
import requests
from PIL import ImageGrab
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client
from apscheduler.schedulers.blocking import BlockingScheduler




## Initializations

# 1) Initializing the program...
print('Initializing the program...')


# Dictionary of articles and corresponding URLs
article_dict = {
    'Samsung 34"': 'https://www.melectronics.ch/de/p/785300157362/samsung-lc34h890wguxen-34-display',
    'Samsung 43"': 'https://www.melectronics.ch/de/p/785300138821/samsung-lc43j890dkux-monitor'
}


# Whatsapp automation using Twilio API
# Cf.:
# YouTube video "How to Send a WhatsApp Message with Python" (https://www.youtube.com/watch?v=98OewpG8-yw)
# Twilio website: https://www.twilio.com/console/sms/whatsapp/learn
def whatsapp_bot_sendtext(bot_message):
    credentials_text_file = open('credentials.txt')
    lines = credentials_text_file.readlines()
    account_sid = lines[2].replace('\n', '') # Twilio credentials
    auth_token = lines[4].replace('\n', '') # creating a rest client object
    client = Client(account_sid, auth_token) # creating a rest client object
    from_whatsapp_number = lines[6].replace('\n', '') # Twilio from phone number
    to_whatsapp_number = lines[8].replace('\n', '') # My (to) phone number
    credentials_text_file.close()
    client.messages.create(body=bot_message, from_=from_whatsapp_number, to=to_whatsapp_number)


# Telegram automation using the requests python package
# Cf.: https://medium.com/@ManHay_Hong/how-to-create-a-telegram-bot-and-send-messages-with-python-4cf314d9fa3e)
def telegram_bot_sendtext(bot_message):
    credentials_text_file = open('credentials.txt')
    lines = credentials_text_file.readlines()
    bot_token = lines[12].replace('\n', '') # python_automation_2_bot
    bot_chatID = lines[14].replace('\n', '') # I.e. this is my user_id
    credentials_text_file.close()
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


# Initial setup message
# initial_message = '✅ Initial setup done for article-tracking.py!'
# print(initial_message)
# # WhatsApp message
# whatsapp_bot_sendtext(initial_message)
# # Telegram message
# telegram_bot_sendtext(initial_message)




## Main function
def job_function():
    # 1) Setting up Chrome web driver using the predefined functions...
    print('1) Setting up Chrome web driver using the predefined functions...')
    # For PyCharm
    # ------
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--incognito')
    from webdriver_manager.chrome import ChromeDriverManager
    driver = webdriver.Chrome(ChromeDriverManager().install(),
                              chrome_options=chrome_options)
    # Getting the resolution of the screen
    img = ImageGrab.grab()
    screen_width = img.size[0]
    screen_height = img.size[1]
    # Setting the size of the web driver window to half the size of the screen
    window_width = int(screen_width / 4)
    window_height = screen_height
    driver.set_window_size(window_width, window_height)  # (240, 160) # driver.minimize_window() # driver.maximize_window()
    # Positioning the web driver window on the right-hand side of the screen
    driver.set_window_position(window_width, 0)
    # ------

    # For Heroku
    # (cf.: https://www.youtube.com/watch?v=Ven-pqwk3ec)
    # ------
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # ------


    # 2) Navigating to the melectronics website and checking the availability of the articles
    print('2) Navigating to the melectronics website and checking the availability of the articles')
    # Reinitializing the string message
    message = ''
    # Looping over the dictionary of articles
    for key in article_dict:
        name = key
        url = article_dict[key]
        try:
            driver.get(url) # launching Chrome on the website we want
            try:
                # Checking Online-Shop availability
                availability_online_string_encoded = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/main/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/span')))
                availability_online_string = availability_online_string_encoded.text
                # Checking Subsidiary availability
                availability_subsidiary_string_encoded = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/main/div/div[1]/div/div[2]/div[3]/div/div/div[2]/div[1]/span')))
                availability_subsidiary_string = availability_subsidiary_string_encoded.text
                # Adding information to the message
                message += '\nᐅ ' + name + ':\n      - ' + availability_online_string + '\n      - ' + availability_subsidiary_string + '\n      - URL: ' + url + '\n'
            except Exception as e:
                message += '\nᐅ ' + name + ':\n      - ⚠️ An error occured, this article might not be available anymore on the website. \n       → Error message: ' + str(e) + '\n      - URL: ' + url + '\n'

        except Exception as e:
            error_message = "⚠️ Either some or all the melectronics URLs are not available or the XPATH leading to the information of interest has been updated. Error message: {0}".format(e)
            print(error_message)
            # WhatsApp message
            whatsapp_bot_sendtext(error_message)
            # Telegram message
            telegram_bot_sendtext(error_message)
            # Exiting the for loop
            break


    # 3) Sending Whatsapp and Telegram message to Anthony
    print('3) Sending Whatsapp and Telegram message to Anthony')
    print(' Message sent to Anthony:\n', message)
    whatsapp_bot_sendtext(message)
    telegram_bot_sendtext(message)


    # 4) Quitting the web driver
    print('4) Quitting the web driver\n\n')
    driver.quit()




## Scheduling job_function to be called
sched = BlockingScheduler()
sched.add_job(func=job_function, trigger='interval', seconds=20)  # hours=12 # weeks=1
sched.start()