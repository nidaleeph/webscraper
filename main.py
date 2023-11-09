import time
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

chrome_options = Options()
chrome_options.add_argument('--lang=en_US')

# For Linux Problems
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-using")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
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

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admindasca",
  port="3306",
  database="teracrome_network_monitor"
)

def DascaCableScraper():

    # Change path to location of chromedriver and chrome_options to desired parameters
    driver = webdriver.Chrome(r"C:\Users\IT\Desktop\chromedriver.exe", options=chrome_options)

    # Link of site needed to be scraped
    driver.get("https://10.255.77.180:31943/unisso/login.action?service=%2Funisess%2Fv1%2Fauth%3Fservice%3D%252Fnmsnetworkmgrwebsite%252Fv1%252Fwebswing%252Findexforwebswing.html%253Ffbclid%253DIwAR341AzzT7f7q5tPrMt02MPM9Ek3nijbRtpZy0SYi4veej9TFwZDaY7V21w#page=UExBVElOVU1fT0xUMigxMC4yNTUuNzcuMjMzKSUyNiUyNmlzU3dpbmdPcGVuJTI2JTI2Mg==")
    driver.maximize_window()
    time.sleep(1.5)
    advance = driver.find_element_by_id("details-button")
    advance.click()
    proceed = driver.find_element_by_id("proceed-link")
    proceed.click()
    username = "admin"
    password = "DascaCable@101"

    time.sleep(1.5)

    user_input = driver.find_element_by_id('username')
    user_input.send_keys(username)
    user_input.send_keys(Keys.ENTER)
    time.sleep(1.5)

    pass_input = driver.find_element_by_id('value')
    pass_input.send_keys(password)
    pass_input.send_keys(Keys.ENTER)
    time.sleep(1.5)

    agree = driver.find_element_by_id("login_warn_confirm")
    agree.click()
    time.sleep(20)

    # Click IT ROOM
    action = webdriver.common.action_chains.ActionChains(driver)

    el = driver.find_element_by_xpath("//div[@id='u2_tab_10000']")
    action.move_to_element_with_offset(el, 637, 139).double_click().perform()
    time.sleep(10)

    # Click GPON Management
    action.reset_actions()
    action.move_to_element_with_offset(el, 50, 180).double_click().perform()
    time.sleep(1)

    action.reset_actions()
    action.move_to_element_with_offset(el, 96, 200).click().perform()

    # Click GPON ONU
    time.sleep(2)
    action.reset_actions()
    action.move_to_element_with_offset(el, 413, 49).click().perform()

    time.sleep(1.5)

    # Click Find
    action.reset_actions()
    action.move_to_element_with_offset(el, 1837, 80).click().perform()

    time.sleep(5)

    # Unit is number of Devices to scrape
    unit = 4
    for i in range(unit):
        # Click Device
        # action.reset_actions()
        # action.move_to_element_with_offset(el, 777, 168).click().perform()

        action.reset_actions()
        action.move_to_element_with_offset(el, 777, 128 + (i * 20)).click().perform()

        # Click Show More
        action.reset_actions()
        action.move_to_element_with_offset(el, 514, 441).click().perform()

        time.sleep(2)

        # Click Running Info
        action.reset_actions()
        action.move_to_element_with_offset(el, 460, 476).click().perform()

        time.sleep(1)

        # Click Running Status

        action.reset_actions()
        action.move_to_element_with_offset(el, 387, 533).click().send_keys(Keys.CONTROL, 'c').perform()
        time.sleep(1)
        action.key_down(Keys.CONTROL)
        action.send_keys("c")
        action.key_up(Keys.CONTROL)
        action.perform()
        status = pyperclip.paste()

        time.sleep(2)

        # Click Optics Module Info Tab
        action.reset_actions()
        action.move_to_element_with_offset(el, 858, 476).click().perform()
        time.sleep(2)

        action.reset_actions()
        action.send_keys(Keys.PAGE_UP).perform()
        time.sleep(1)

        # Highlight the Temperature and Voltage
        action.reset_actions()
        action.move_to_element_with_offset(el, 387, 533).click().send_keys(Keys.CONTROL, 'c').perform()
        time.sleep(1)
        action.key_down(Keys.CONTROL)
        action.send_keys("c")
        action.key_up(Keys.CONTROL)
        action.perform()
        temperature = pyperclip.paste()

        action.reset_actions()
        action.send_keys(Keys.PAGE_DOWN).perform()

        time.sleep(1)
        action.reset_actions()
        action.send_keys(Keys.ARROW_DOWN)
        action.send_keys(Keys.CONTROL, 'c')
        action.perform()

        time.sleep(1)
        action.key_down(Keys.CONTROL)
        action.send_keys("c")
        action.key_up(Keys.CONTROL)
        action.perform()
        voltage = pyperclip.paste()
        time.sleep(2)
        print(status, temperature, voltage)


    driver.quit()

def DascaSpecificCrawler(sin_lst):

    # Change path to location of chromedriver and chrome_options to desired parameters
    driver = webdriver.Chrome(r"C:\Users\IT\Desktop\chromedriver.exe", options=chrome_options)

    # Link of site needed to be scraped
    driver.get("https://10.255.77.180:31943/unisso/login.action?service=%2Funisess%2Fv1%2Fauth%3Fservice%3D%252Fnmsnetworkmgrwebsite%252Fv1%252Fwebswing%252Findexforwebswing.html%253Ffbclid%253DIwAR341AzzT7f7q5tPrMt02MPM9Ek3nijbRtpZy0SYi4veej9TFwZDaY7V21w#page=UExBVElOVU1fT0xUMigxMC4yNTUuNzcuMjMzKSUyNiUyNmlzU3dpbmdPcGVuJTI2JTI2Mg==")
    driver.maximize_window()
    username = "admin"
    password = "DascaCable@101"

    time.sleep(1.5)
    advance = driver.find_element_by_id("details-button")
    advance.click()
    proceed = driver.find_element_by_id("proceed-link")
    proceed.click()
    time.sleep(1.5)

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

    time.sleep(15)
    action = webdriver.common.action_chains.ActionChains(driver)


    action.move_to_element(driver.find_element_by_id("search")).click()
    action.send_keys("0")
    action.perform()
    action.reset_actions()
    time.sleep(0.5)
    action.send_keys(Keys.ENTER).perform()
    action.reset_actions()

    time.sleep(2.5)

    el = driver.find_element_by_xpath("//div[@id='u2_tab_10000']")
    action.move_to_element_with_offset(el, 1052, 84).click().perform()
    action.reset_actions()

    for i in sin_lst:

        time.sleep(2.5)
        # Already in ONU searcher
        action.move_to_element_with_offset(el, 731, 120).click()
        action.send_keys(i)
        action.send_keys(Keys.ENTER)
        action.perform()
        action.reset_actions()
        time.sleep(1)

        # Click the Device
        action.move_to_element_with_offset(el, 470, 290).click().perform()
        action.reset_actions()

        time.sleep(7)

        # Click advanced
        action.move_to_element_with_offset(el, 1770, 456).click().perform()
        action.reset_actions()

        time.sleep(1)

        # Click running info
        action.move_to_element_with_offset(el, 780, 286).click().perform()
        action.reset_actions()

        time.sleep(0.5)

        # Click Running Status

        action.move_to_element_with_offset(el, 768, 343).click().send_keys(Keys.CONTROL, 'c').perform()
        time.sleep(0.5)
        action.key_down(Keys.CONTROL)
        action.send_keys("c")
        action.key_up(Keys.CONTROL)
        action.perform()
        status = pyperclip.paste()

        time.sleep(1)

        # Click Optics Module Info Tab
        action.reset_actions()
        action.move_to_element_with_offset(el, 984, 286).click().perform()
        time.sleep(1)

        action.reset_actions()
        action.send_keys(Keys.PAGE_UP).perform()
        time.sleep(0.5)

        # Highlight the Temperature and Voltage
        action.reset_actions()
        action.move_to_element_with_offset(el, 872, 343).click().send_keys(Keys.CONTROL, 'c').perform()
        time.sleep(0.5)
        action.key_down(Keys.CONTROL)
        action.send_keys("c")
        action.key_up(Keys.CONTROL)
        action.perform()
        temperature = pyperclip.paste()

        action.reset_actions()
        action.send_keys(Keys.PAGE_DOWN).perform()

        time.sleep(0.5)
        action.reset_actions()
        action.send_keys(Keys.CONTROL, 'c')
        action.perform()

        time.sleep(0.5)
        action.key_down(Keys.CONTROL)
        action.send_keys("c")
        action.key_up(Keys.CONTROL)
        action.perform()
        voltage = pyperclip.paste()
        action.reset_actions()
        time.sleep(1)
        print(status, temperature, voltage)

        # Exit advanced and go to next ONU
        close = driver.find_elements_by_class_name("ev_tab_closeSpan ")[-1]
        close.click()

        time.sleep(0.5)

        resource_tab = driver.find_element_by_id("ev_tabItem_10001")
        resource_tab.click()

        # datetime object containing current date and time
        now = datetime.now()

        # dd/mm/YY H:M:S
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

        status = status.split("=\t")
        temperature = temperature.split("=\t")
        voltage = voltage.split("=\t")

        status = status[1]
        temperature = temperature[1]
        voltage = voltage[1]

        json = {
            "status": status,
            "temperature": temperature,
            "voltage_power": voltage,
            "onu_serial_number": i
        }

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
    driver.quit()


DascaSpecificCrawler(["48575443ABFC4FA4", "4857544302EC39A5"])