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

# # For Linux Problems
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-using")
# user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument(f'user-agent={user_agent}')
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--window-size=1920x1080")
# chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--disable-features=VizDisplayCompositor")
# # chrome_options.add_argument("--headless")
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--dns-prefetch-disable")

# # chrome_prefs = {}
# # chrome_options.experimental_options["prefs"] = chrome_prefs
# # chrome_prefs["profile.default_content_settings"] = {"images": 2}
# # chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

# chrome_options.add_experimental_option('w3c', False)

chrome_options.add_argument('--lang=en_US')

# For Linux Problems
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")
chrome_options.add_argument('--ignore-certificate-errors')

chrome_options.add_argument("--start-maximized")
# chrome_options.add_experimental_option('w3c', False)

chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 20}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 20}


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admindasca",
    port="3306",
    database="teracrome_network_monitor"
)

arr_queue = []
running_queue = []
app = Flask(__name__)


def queue(serialNumber):
    global arr_queue
    arr_queue.append(serialNumber)
    return proccess_queue(serialNumber)


def proccess_queue(serial):
    global arr_queue
    global running_queue
    while 1:
        this_index = arr_queue.index(serial)
        if this_index == 0:
            if len(running_queue) <= 2 and len(arr_queue) != 0:
                print("Getting Modem info for modem: ", serial)
                index = arr_queue.index(serial)
                serial_number = arr_queue.pop(index)
                running_queue.append("Proccessing")
                queue = multiprocessing.Queue()
                p1 = Process(target=DascaSpecificCrawler, args=(serial_number, queue))
                p1.start()
                p1.join()
                running_queue.pop(0)
                return (queue.get())


def DascaSpecificCrawler(serialNumber, queue):
    # Change path to location of chromedriver and chrome_options to desired parameters
    driver = webdriver.Chrome(r"C:\Users\IT\chromeDriver\chromedriver.exe", options=chrome_options)
    # driver = webdriver.Chrome(r"C:\Users\IT\Desktop\chromedriver.exe", options=chrome_options)

    # Link of site needed to be scraped
    driver.get(
        "https://10.255.77.180:31943/unisso/login.action?service=%2Funisess%2Fv1%2Fauth%3Fservice%3D%252Fnmsnetworkmgrwebsite%252Fv1%252Fwebswing%252Findexforwebswing.html%253Ffbclid%253DIwAR341AzzT7f7q5tPrMt02MPM9Ek3nijbRtpZy0SYi4veej9TFwZDaY7V21w#page=UExBVElOVU1fT0xUMigxMC4yNTUuNzcuMjMzKSUyNiUyNmlzU3dpbmdPcGVuJTI2JTI2Mg==")
    driver.maximize_window()
    try:
        username = "admin"
        password = "DascaCable@101"

        time.sleep(1.5)
        # advance = driver.find_element_by_id("details-button")
        # advance.click()
        # proceed = driver.find_element_by_id("proceed-link")
        # proceed.click()
        # time.sleep(1.5)

        user_input = driver.find_element_by_id('username')
        user_input.send_keys(username)
        user_input.send_keys(Keys.ENTER)
        time.sleep(1.5)

        pass_input = driver.find_element_by_id('value')
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.ENTER)

        time.sleep(2)

        agree = driver.find_element_by_id("login_warn_confirm")
        agree.click()

        time.sleep(20)
        action = webdriver.common.action_chains.ActionChains(driver)
        

        driver.get(
            "https://10.255.77.180:31943/nmsnetworkmgrwebsite/v1/webswing/indexforwebswing.html#page=SHJlZiUzRCUyRnBoeWludm1ncndlYnNpdGUlMkZ2MSUyRmZ1bGx0ZXh0c2VhcmNoJTJGZGlzdCUyRmluZGV4Lmh0bWwlM0Z2YWx1ZSUzRDAlMjZyZWZyLWZsYWdzJTNEZSUyNnRpdGxlJTNEZnVsbHRleHRzZWFyY2glMjZvcGVuVHlwZSUzRHJlbG9hZCUyNnNwYVRhYklkJTNEUmVzb3VyY2UlMjBTZWFyY2glMjZzcGFUYWJUaXRsZSUzRFJlc291cmNlJTIwU2VhcmNo")
        driver.maximize_window()
        time.sleep(5)
        # element = driver.find_element_by_id("search")
        # element.click()

        # el2 = driver.find_element_by_id("")
        # el2.send_keys("0")
        # el2.send_keys(Keys.ENTER)

        # action.move_to_element(driver.find_element_by_id("search")).click().perform()
        # action.reset_actions()
        # time.sleep(2)
        # action.send_keys("0").perform()
        # # action.perform()
        # action.reset_actions()
        # time.sleep(2)
        # action.send_keys(Keys.ENTER).perform()
        # action.reset_actions()

        print("Finding Serial Number")

        el = driver.find_element_by_xpath("//div[@id='u2_tab_10000']")
        # action.find_element_by_id("webtopo_search_topo_select_item_ONU").click().perform()
        action.move_to_element_with_offset(el, 975, 84).click().perform()
        action.reset_actions()
        time.sleep(2.5)
        action.move_to_element_with_offset(el, 605, 225).click().perform()
        action.reset_actions()

        time.sleep(2.5)
        # Already in ONU searcher
        action.move_to_element_with_offset(el, 975, 120).click()
        action.send_keys(serialNumber)
        action.send_keys(Keys.ENTER)
        action.perform()
        action.reset_actions()
        time.sleep(1)

        print("Clicking the Device")

        # Click the Device
        # action.move_to_element_with_offset(el, 330, 400).double_click().send_keys(Keys.CONTROL, 'c').perform()
        # time.sleep(0.5)
        # action.key_down(Keys.CONTROL)
        # action.send_keys("c")
        # action.key_up(Keys.CONTROL)
        # action.perform()
        # test = pyperclip.paste()
        # action.reset_actions()
        # print(test)
        # time.sleep(20)
        action.move_to_element_with_offset(el, 470, 465).click().perform()
        action.reset_actions()

        time.sleep(10)

        # Click advanced
        action.move_to_element_with_offset(el, 1770, 456).click().perform()
        action.reset_actions()

        time.sleep(1)

        # Click running info
        action.move_to_element_with_offset(el, 780, 286).click().perform()
        action.reset_actions()

        time.sleep(5)

        # Click Running Status

        print("Getting Status")

        action.move_to_element_with_offset(el, 768, 343).click().send_keys(Keys.CONTROL, 'c').perform()
        time.sleep(5)
        action.key_down(Keys.CONTROL)
        action.send_keys("c")
        action.key_up(Keys.CONTROL)
        action.perform()
        status = pyperclip.paste()

        time.sleep(3)

        # Click Optics Module Info Tab
        action.reset_actions()
        action.move_to_element_with_offset(el, 984, 286).click().perform()
        time.sleep(3)

        action.reset_actions()
        action.send_keys(Keys.PAGE_UP).perform()
        time.sleep(5)

        # Highlight the Temperature and Voltage
        action.reset_actions()
        action.move_to_element_with_offset(el, 872, 343).click().send_keys(Keys.CONTROL, 'c').perform()
        time.sleep(5)
        action.key_down(Keys.CONTROL)
        action.send_keys("c")
        action.key_up(Keys.CONTROL)
        action.perform()
        temperature = pyperclip.paste()

        action.reset_actions()
        action.send_keys(Keys.PAGE_DOWN).perform()

        time.sleep(5)
        action.reset_actions()
        action.send_keys(Keys.CONTROL, 'c')
        action.perform()

        time.sleep(5)
        action.key_down(Keys.CONTROL)
        action.send_keys("c")
        action.key_up(Keys.CONTROL)
        action.perform()
        voltage = pyperclip.paste()
        action.reset_actions()
        # print(serialNumber, status, temperature, voltage)
        print(status)
        print("Parsing Data")
        time.sleep(10)

        # datetime object containing current date and time
        now = datetime.now()

        # dd/mm/YY H:M:S
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        if status is not None:
            print(status)
            status = status.split("=\t")
            if status[1]:
                status = status[1]
            else:
                status = None
        if temperature is not None:
            print(temperature)
            temperature = temperature.split("=\t")
            if temperature[1]:
                temperature = temperature[1]
            else:
                temperature = None
        if voltage is not None:
            print(voltage)
            voltage = voltage.split("=\t")
            if voltage[1]:
                voltage = voltage[1]
            else:
                voltage = None

        json = {
            "status": status,
            "temperature": temperature,
            "voltage_power": voltage,
            "onu_serial_number": serialNumber
        }

        queue.put(json)

        print("Saving Data")

        mycursor = mydb.cursor()
        mycursor.execute("""
            INSERT INTO onu
                (onu_serial_number, status, voltage_power, temperature, updatedAt)
            VALUES
                (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                                                -- no need to update the PK
                status  = VALUES(status),
                temperature  = VALUES(temperature),
                voltage_power   = VALUES(voltage_power),
                updatedAt   = VALUES(updatedAt);
                        """, (
            json['onu_serial_number'], json['status'], json['voltage_power'], json['temperature'], dt_string)
                         # python variables
                         )
        mydb.commit()
        queue.put(serialNumber)
        driver.quit()
    except NameError:
        error_mes = {
            'Error': "1",
            'message': NameError
        }
        # print(NameError)
        queue.put(error_mes)
        driver.quit()

    # except:
    #     error_mes = {
    #         'Error': "1",
    #         'message': "Something else went wrong"
    #     }
    #     # print(NameError)
    #     queue.put(error_mes)
    #     driver.quit()


@app.route('/webscrape', methods=['POST', 'GET'])
def index():
    try:
        content = request.json
        x = queue(content['serialNumber'])
        return {'x': x}
    except:
        return {'Error': "Something went Wrong"}


if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=8000)
