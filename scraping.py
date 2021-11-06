import uuid
import logging

from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

start_datetime = datetime.today().strftime('%Y.%m.%d.%H:%M')
print(start_datetime)
logging.basicConfig(filename='logging_info.txt', level=logging.INFO)

url = 'https://www.reddit.com/top/?t=month'

"""
Please enter your driver pass into executable_path='' variable
"""
driver = webdriver.Chrome(
    executable_path='')
driver.implicitly_wait(300)
driver.get(url)

last_height = driver.execute_script("return document.body.scrollHeight")
link_set = set()

logging.info(u'Start parsing 100 post links')


def parse_hundred_href():
    post_urls = driver.find_elements(By.CLASS_NAME, '_3jOxDPIQ0KaOWpzvSQo-1s')
    for post_url in post_urls:
        post_link = post_url.get_attribute('href')
        if len(link_set) >= 100:
            return True

        link_set.add(post_link)


while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    result = parse_hundred_href()
    if result:
        break
    new_height = driver.execute_script("return document.body.scrollHeight")
    last_height = new_height

link_list = list(link_set)


logging.info(u'Start scraping info')
for link in link_list:
    url = link
    driver.get(url)
    logging.info(u'Open each post and scrape date, comments, votes, category, author, link to author profile')
    UID = uuid.uuid1().hex

    date_posted = driver.find_element(By.CLASS_NAME, '_3jOxDPIQ0KaOWpzvSQo-1s')
    ActionChains(driver).move_to_element(date_posted).perform()
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    full_date = soup.find(class_='_2J_zB4R1FH2EjGMkQjedwc u6HtAZu8_LKL721-EnKuR')

    comments = soup.find(class_='FHCV02u6Cp2zYL0fhQPsO')

    votes = soup.find(class_='_1E9mcoVn4MYnuBQSVDt1gC')

    category = soup.find(class_='_19bCWnxeTjqzBElWZfIlJb')

    user_profile = soup.find(class_='_2mHuuvyV9doV3zwbZPtIPG')
    user_a = user_profile.find('a')
    user_url_name = user_a['href']
    user_url = 'https://www.reddit.com' + str(user_url_name)

    logging.info(u'Move to user profile, scrape karma and cake day; Print info')
    url = user_url
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    if soup.find(class_='bDDEX4BSkswHAG_45VkFB'):
        continue

    else:
        karma = driver.find_element(By.CLASS_NAME, '_1hNyZSklmcC7R_IfCUcXmZ')
        ActionChains(driver).move_to_element(karma).perform()
        wait_for_karma = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, '_3uK2I0hi3JFTKnMUFHD2Pd')))
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        full_karma = soup.find(class_='_3uK2I0hi3JFTKnMUFHD2Pd')

        user_cake_day = soup.find(id='profile--id-card--highlight-tooltip--cakeday')

        with open(str(start_datetime) + '.txt', 'a') as file:
            file.write('id: ' + str(UID) + '\n')
            file.write('post link: ' + str(link) + '\n')
            file.write('username: ' + str(user_url_name) + '\n')
            file.write('cake day: ' + str(user_cake_day.text) + '\n')
            file.write('karma: ' + str(full_karma.text) + '\n')
            file.write('posted on: ' + str(full_date.text) + '\n')
            file.write('number of comments: ' + str(comments.text) + '\n')
            file.write('number of votes: ' + str(votes.text) + '\n')
            file.write('category: ' + str(category.text) + '\n' + '\n')


driver.quit()
stop_datetime = datetime.today().strftime('%Y.%m.%d.%H:%M')
print(stop_datetime)
