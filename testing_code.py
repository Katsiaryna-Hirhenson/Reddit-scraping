from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.action_chains import ActionChains

url = 'https://www.reddit.com/user/hestolemysmile/'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}

driver = Chrome(executable_path='/Users/ekaterinagirgenson/Proga/PycharmProjects/reddit_scraping/chromedriver')
driver.get(url)

time.sleep(10)
date_posted = driver.find_element(By.CLASS_NAME, '_1hNyZSklmcC7R_IfCUcXmZ')
ActionChains(driver).move_to_element(date_posted).perform()
time.sleep(20)


html_data = requests.get(url=url, headers=headers)
soup = BeautifulSoup(html_data.content, 'lxml')

user_karma = soup.find("span",
                                       id=("profile--id-card--highlight-"
                                           "tooltip--karma")).text

print(user_karma)