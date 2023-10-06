from selenium import webdriver

# Create a new instance of the Chrome driver (you should replace this with the path to your WebDriver executable)
driver = webdriver.Chrome('"C:/Program Files/Google/Chrome/Application/chrome.exe"')

# Navigate to the URL of the web page you want to scrape
url = 'https://www.nhatot.com/mua-ban-can-ho-chung-cu-quan-7-tp-ho-chi-minh?page=14'
driver.get(url)

# Wait for a few seconds to ensure the page is fully loaded (you can adjust the wait time as needed)
import time
time.sleep(5)

# Get the page source (HTML) after it has fully loaded
page_source = driver.page_source

# Now, you can work with the page_source as needed
# For example, you can parse it using a library like BeautifulSoup
from bs4 import BeautifulSoup

soup = BeautifulSoup(page_source, 'html.parser')

# Find and print the title of the page
title = soup.find('title')
if title:
    print("Page Title:", title.text)
else:
    print("Title not found on the page")

# Finally, don't forget to close the browser when you're done
driver.quit()
