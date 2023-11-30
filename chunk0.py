from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time
#import pandas as pd
import schedule


import datetime
import pytz

def get_zone_specific_time(zone_name):
    # Get the current time in UTC
    utc_now = datetime.datetime.utcnow()

    # Specify the time zone using the pytz library
    target_zone = pytz.timezone(zone_name)

    # Convert the UTC time to the target time zone
    zone_specific_time = utc_now.replace(tzinfo=pytz.utc).astimezone(target_zone)

    return zone_specific_time

# Example usage: Get the current time in New York
la_time = get_zone_specific_time('America/Los_Angeles')
print(f"Current time in LA: {la_time}")



'''

def scrape_job():


    try:
    
        # URL of the website you want to scrape
        url = 'https://www.espn.com/'
        print(url)
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        # Create a Chrome WebDriver instance with the Service object
        #chrome_path = 'C:/Users/theri/anaconda3/envs/selenium/Lib/site-packages/selenium/webdriver/common/windows'


        driver = webdriver.Chrome()
        print("Assigned Chrome Driver")

        # Open the websit
        driver.get(url)
        print(f"Accessing: {url}")

        # assign ESPN.com's headline stack to a variable using its XPATH
        headline_stack = WebDriverWait(driver,4).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="main-container"]/div/section[3]/div[1]/section/ul')))
        print("Extracted HeadLine Stack")

        # extract text (headlines) from the element and separate the headlines using \n to split on.
        headline_txt = headline_stack.text.split('\n')
        print("Extracted Headline Text")

        # close the driver
        driver.close

        # assign first (top) headline to variable
        top_headline = headline_txt[0]
        print(top_headline)

        #get timestamp

        
        return(top_headline)
    

    
    except Exception as e:
        
        print(f"An error occurred: {e}")
        
        
        
               
schedule.every(1).minute.do(scrape_job)



while True:
    schedule.run_pending()
    time.sleep(4)

'''