# Creating a Web server using Python and Flask
# python -m http.server 8000 --bind 127.0.0.1
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
import pyperclip
import mysql.connector
from datetime import datetime

import multiprocessing
from flask import Flask, jsonify, request
from multiprocessing import Value, Array, Manager, Process, Queue
from ctypes import c_wchar_p
import time
import sys

chrome_options = Options()
# chrome_options.add_argument('--lang=en_US')

# For Linux Problems
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-using")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--disable-features=VizDisplayCompositor")
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--dns-prefetch-disable")

# chrome_prefs = {}
# chrome_options.experimental_options["prefs"] = chrome_prefs
# chrome_prefs["profile.default_content_settings"] = {"images": 2}
# chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

chrome_options.add_experimental_option('w3c', False)

# chrome_options.add_argument("--window-size=1920,1080")
# # chrome_options.add_argument("--disable-extensions")
# # chrome_options.add_argument("--proxy-server='direct://'")
# # chrome_options.add_argument("--proxy-bypass-list=*")
# chrome_options.add_argument("--start-maximized")
# # chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# # chrome_options.add_argument('--disable-dev-shm-usage')
# # chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--ignore-certificate-errors')
# # chrome_options.browser = webdriver.Chrome(options=chrome_options.chrome_options)


def DascaSpecificCrawler():
    # Change path to location of chromedriver and chrome_options to desired parameters
    driver = webdriver.Chrome(r"D:\Chrome  Driver\96\chromedriver.exe", options=chrome_options)

    # Link of site needed to be scraped
    driver.get(
        "https://www.google.com")
    driver.maximize_window()

    action = webdriver.common.action_chains.ActionChains(driver)

    # el = driver.find_element_by_xpath("//div[contains(@class, 'RNNXgb')]")
    action.move_to_element(driver.find_element_by_class_name("RNNXgb")).perform()
    el = driver.find_element_by_class_name("RNNXgb")
    print(el)
    action.move_to_element_with_offset(el, 50, 50).click().perform()
    action.reset_actions()
    action.move_to_element_with_offset(el, 810, 588).click().send_keys(Keys.CONTROL, 'c').perform()
    time.sleep(0.5)
    action.key_down(Keys.CONTROL)
    action.send_keys("c")
    action.key_up(Keys.CONTROL)
    action.perform()
    test = pyperclip.paste()

    action.reset_actions()


    print(test)
        


DascaSpecificCrawler()