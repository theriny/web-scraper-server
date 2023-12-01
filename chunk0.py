from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time
import pandas as pd
import schedule


import datetime
import pytz


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import os

def send_email(arg1):
    # Email configuration
    sender_email = "therin.young@gmail.com"
    receiver_email = "ceo@dataexplorers.co"
    subject = "CSV File Attachment"
    body = "Please find the attached CSV file."

    # Gmail SMTP server settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "therin.young@gmail.com"
    smtp_password = "bfzh wjxs gxud nfmg"

    # File to be attached
    attachment_path = arg1

    # Create the MIME object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Attach the file
    attachment = open(attachment_path, "rb")
    base = MIMEBase("application", "octet-stream")
    base.set_payload((attachment).read())
    encoders.encode_base64(base)
    base.add_header("Content-Disposition", f"attachment; filename= {attachment_path}")
    message.attach(base)

    # Establish a connection to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Email sent successfully!")


def get_zone_specific_time(zone_name):
    # Get the current time in UTC
    utc_now = datetime.datetime.utcnow()

    # Specify the time zone using the pytz library
    target_zone = pytz.timezone(zone_name)

    # Convert the UTC time to the target time zone
    zone_specific_time = utc_now.replace(tzinfo=pytz.utc).astimezone(target_zone)

    return zone_specific_time






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
        current_time = get_zone_specific_time('America/New_York')


        # Determine if resutls.csv already exists
        file_path = "results.csv"

        if os.path.exists(file_path):
            print(f"The file {file_path} exists.")

            # read in file
            df = pd.read_csv(file_path)

            for headlines in headline_txt:
                if headlines not in list(df['top_headline']):
                    df.loc[len(df),'top_headline'] = headlines
                    df.loc[len(df)-1,'timestamp'] = current_time

                else:
                    print(f'Headline: {headlines} is already present.')

            df.to_csv('results.csv',index=False)

        else:
            print(f"The file {file_path} does not exist.")

            #empty dataframe
            df = pd.DataFrame()


            df['top_headline'] = [headline_txt]
            df['timestamp'] = [current_time]

            df.to_csv('results.csv',index=False)


        send_email('results.csv')
        
        return(top_headline)
    

    
    except Exception as e:
        
        print(f"An error occurred: {e}")
        
        
        
               
schedule.every(1).minute.do(scrape_job)



while True:
    schedule.run_pending()
    time.sleep(4)

