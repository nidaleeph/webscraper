import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import pyperclip

chrome_options = Options()
chrome_options.add_argument('--lang=en_US')

# For Linux Problems
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")

chrome_options.add_argument("--start-maximized")

# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-using")
# chrome_options.add_argument("--disable-features=VizDisplayCompositor")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--dns-prefetch-disable")

chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
chrome_options.add_experimental_option('w3c', False)

# Change COMMAND to CONTROL
# Change move_to_element_with_offset if not working
def google_crawler():
    google_driver = webdriver.Chrome("D:\Chrome  Driver\96\chromedriver.exe", options=chrome_options)
    google_driver.get(
        "https://www.google.com/search?q=paper&ei=Ski4YZWIK9aXr7wPvbCNgAc&ved=0ahUKEwiV1dfo4uL0AhXWy4sBHT1YA3AQ4dUDCA4&uact=5&oq=paper&gs_lcp=Cgdnd3Mtd2l6EAMyBwgAELEDEEMyBwgAELEDEEMyBAgAEEMyBAguEEMyCgguELEDEIMBEEMyCAgAEIAEELEDMggIABCABBCxAzIOCC4QgAQQsQMQxwEQ0QMyBQgAEIAEMgUIABCxAzoHCAAQRxCwAzoHCAAQsAMQQzoICAAQ5AIQsAM6CgguEMgDELADEEM6EAguEMcBEKMCEMgDELADEENKBAhBGABKBAhGGAFQ-QVY-QVg3QdoAXACeACAAViIAViSAQExmAEAoAEByAETwAEB&sclient=gws-wiz")

    time.sleep(3)

    action = webdriver.common.action_chains.ActionChains(google_driver)
    el = google_driver.find_element_by_xpath("//div[@id='sfcnt']")

    print(el)
    action.reset_actions()
    action.move_to_element_with_offset(el, 0, 0).click_and_hold().move_to_element_with_offset(el, 900, 800)
    time.sleep(1)
    action.key_down(Keys.CONTROL)
    action.send_keys("c")
    action.perform()
    page = pyperclip.paste()
    google_driver.close()
    print("test")
    print(page)

    print("DONE")

google_crawler()