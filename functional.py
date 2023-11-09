import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
browser = webdriver.Firefox()

url = 'https://iol1.iroquois.com/infopost/Pages/OperationallyAvailable.php?parentId=100'
browser.get(url)
WebDriverWait(browser,10000).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
date_element = browser.find_element_by_id('searchDateTextfield-inputEl')
date_element.click()
date_element.send_keys(Keys.HOME)

# For date 10 Oct 2015
date_element.send_keys("10042015")
date_element.send_keys(Keys.TAB)
browser.find_element_by_xpath("//span[@id='retrieveButton-btnInnerEl']").click()
time.sleep(100)
browser.close()