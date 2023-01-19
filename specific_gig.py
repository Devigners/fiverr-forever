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

# Start Chrome with the remote debugging port option
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Connect to the existing Chrome instance using Selenium
driver = webdriver.Chrome(options=chrome_options)

# Opening JSON file
with open('data.json') as json_file:
    data = json.load(json_file)
    
for user_rank in list(data.keys()):
    if data[user_rank]['seller']['name'] == 'saifullahkhaki':
        break
    
    gig_link = data[user_rank]['href']
    
    print('[FETCHING]: '+gig_link)
    while(True):
        driver.get(gig_link)
        if(driver.title != 'Your Access To This Website Has Been Blocked'):
            wait = WebDriverWait(driver, 10)
            
            # downloading thumbnail images for affiliate marketing
            gig_images = driver.find_elements('css selector', 'figure.thumbnail img')
            data[user_rank]['images'] = []
            urls = []
            for image in gig_images:
                img_url = image.get_attribute('src')
                if img_url not in urls:
                    urls.append(img_url)
                    img_data = requests.get(img_url).content
                    with open('Gig Images/'+str(user_rank)+' - '+str(gig_images.index(image))+' - '+data[user_rank]['title']+'.jpg', "wb") as handler:
                        handler.write(img_data)
                        data[user_rank]['images'].append('Gig Images/'+str(user_rank)+' - '+str(gig_images.index(image))+' - '+data[user_rank]['title']+'.jpg')
                        
                        print('[DOWNLOADING]: '+'Gig Images/'+str(user_rank)+' - '+str(gig_images.index(image))+' - '+data[user_rank]['title']+'.jpg')
                        
            # find their selected options for categories and inside
            data[user_rank]['options'] = {}
            data[user_rank]['options']['categories'] = []
            gig_category_breadcrumbs = driver.find_elements('css selector', '.category-breadcrumbs a')
            for breadcrumb in gig_category_breadcrumbs:
                data[user_rank]['options']['categories'].append(breadcrumb.text)
                
            data[user_rank]['options']['meta'] = {}
            gig_meta_sections = driver.find_elements('css selector', '.metadata-attribute')
            for section in gig_meta_sections:
                gig_meta_section_heading = section.find_element('css selector', 'p')
                data[user_rank]['options']['meta'][gig_meta_section_heading.text] = []
                
                gig_meta_section_fields = section.find_elements('css selector', 'li')
                for field in gig_meta_section_fields:
                    data[user_rank]['options']['meta'][gig_meta_section_heading.text].append(field.text)
            
            # getting the tags of the gig
            data[user_rank]['tags'] = []
            gig_tags = driver.find_elements('css selector', '.gig-tags-container a')
            for tag in gig_tags:
                data[user_rank]['tags'].append(tag.text)
            break
        else:
            if input('Is your issue resolved? ') == 'y':
                break 

# Write the JSON string to a file
with open("data_extended.json", "w") as f:
    f.write(json.dumps(data))

# Close the browser
driver.quit()