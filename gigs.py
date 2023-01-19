import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import subprocess
import time
import regex as re
import os
import json
import psutil

# # check if chrome is already running
# def chrome_running():
#     for proc in psutil.process_iter():
#         try:
#             if proc.name() == "chrome.exe":
#                 return True
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#     return False 

# if chrome_running():
#     print("Chrome is running.")
# else:
#     print("Chrome is not running.")
#     subprocess.Popen('chrome.exe -remote-debugging-port=9222 -incognito')
    
#     # start chrome right from
#     time.sleep(5)


# gigs dictionary
gigs_data = {}

# Start Chrome with the remote debugging port option
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Connect to the existing Chrome instance using Selenium
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.fiverr.com/search/gigs?query=flask&page=1')
wait = WebDriverWait(driver, 10)

# select the right currency
# currency-selection-title
# default-currency-item
# currency-name
currency_selector = driver.find_element('css selector', '.currency-selection-title')
currency_selector.click()
wait = WebDriverWait(driver, 10)

currency_buttons = driver.find_elements('css selector', '.default-currency-item')
usd_button = [button for button in currency_buttons if button.find_element('css selector', '.currency-name').text == 'United States Dollar'][0]
usd_button.click()
wait = WebDriverWait(driver, 10)

# refetching the page with corrected currency
driver.get('https://www.fiverr.com/search/gigs?query=flask&page=1&source=pagination&offset=-3')
wait = WebDriverWait(driver, 10)

# page-number or only 3 pages
result_pages = 3
result_pages = driver.find_elements('css selector', '.page-number')

# 1-10
for page_number in range(1, len(result_pages)+1):
    
    # gig-card-layout 
    gigs = driver.find_elements('css selector', '.gig-card-layout')
    for gig in gigs:
        gig_entry_number = 48*(page_number-1)+gigs.index(gig)
        gigs_data[gig_entry_number] = {}
        gigs_data[gig_entry_number]['seller'] = {}
        
        # fetching gig title and link
        a_tag = gig.find_element('css selector', 'h3 a')
        gigs_data[gig_entry_number]['title'] = a_tag.text
        gigs_data[gig_entry_number]['href'] = a_tag.get_attribute('href')
        
        print('[GIG '+ str(gig_entry_number) +' ]: Found for title', gigs_data[gig_entry_number]['title'])
        
        # fetching gig price
        price_gig = gig.find_element('css selector', '.price span')
        gigs_data[gig_entry_number]['price'] = price_gig.text
        
        # fetching gig rating if exist
        try:
            rating_gig = gig.find_element('css selector', '.gig-rating')
            gigs_data[gig_entry_number]['rating'] = rating_gig.text
        except:
            gigs_data[gig_entry_number]['rating'] = '0.0(0)'
    
        # fetching seller name
        seller_gig = gig.find_element('css selector', '.seller-name a')
        gigs_data[gig_entry_number]['seller']['name'] = seller_gig.text
        
        # fetching seller rank
        try:
            seller_rank_gig = gig.find_element('css selector', '.level span')
            gigs_data[gig_entry_number]['seller']['rank'] = seller_rank_gig.text
        except:
            gigs_data[gig_entry_number]['seller']['rank'] = 'None'
        
        
    print('[STATUS]: Page', page_number, 'Done.')
    next_page_url = 'https://www.fiverr.com/search/gigs?query=flask&page='+str((page_number+1))+'&source=pagination&offset=-3'
    driver.get(next_page_url)
    wait = WebDriverWait(driver, 10)


# Write the JSON string to a file
with open("data.json", "w") as f:
    f.write(json.dumps(gigs_data))

# Close the browser
driver.quit()
