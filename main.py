import logging
import uuid
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

logging.basicConfig(filename='logname.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

url = 'https://www.reddit.com/top/?t=month'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('window-size=1200x600')
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument("--headless")

"""
Insert path to your chromedriver into 'executable_path' argument below
"""

driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
driver.implicitly_wait(300)
driver.get(url)

last_height = driver.execute_script('return document.body.scrollHeight')
link_set = set()
row = []
final_result = []


def parse_hundred_href():
    post_urls = driver.find_elements(By.CLASS_NAME, '_3jOxDPIQ0KaOWpzvSQo-1s')
    for post_url in post_urls:
        post_link = post_url.get_attribute('href')
        if len(link_set) >= 100:
            return True

        link_set.add(post_link)


def scraping_data_by_class(class_str, soup):
    data = soup.find(class_=class_str)
    data = data.text
    row.append(data)


scraping_post_profile = {'full_date': '_2J_zB4R1FH2EjGMkQjedwc u6HtAZu8_LKL721-EnKuR',
                         'comments': 'FHCV02u6Cp2zYL0fhQPsO',
                         'votes': '_1E9mcoVn4MYnuBQSVDt1gC',
                         'category': '_19bCWnxeTjqzBElWZfIlJb',
                         }

scraping_user_profile = {'user_cake_day': '_3KNaG9-PoXf4gcuy5_RCVy',
                         'full_karma': '_3uK2I0hi3JFTKnMUFHD2Pd',
                         }


def scraping(link):
    try:
        driver.get(link)
        uid = uuid.uuid1().hex
        row.append(uid)
        date_posted = driver.find_element(By.CLASS_NAME, '_3jOxDPIQ0KaOWpzvSQo-1s')
        ActionChains(driver).move_to_element(date_posted).perform()
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        for value in scraping_post_profile.values():
            scraping_data_by_class(class_str=value, soup=soup)

        # get link to move to user profile
        user_profile = soup.find(class_='_2mHuuvyV9doV3zwbZPtIPG')
        user_a = user_profile.find('a')
        user_url_name = user_a['href']
        row.append(user_url_name)
        user_url = 'https://www.reddit.com' + str(user_url_name)

        driver.get(user_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        # check if you are on "are you over 18" page; if yes, skip this post
        if soup.find(class_='bDDEX4BSkswHAG_45VkFB'):
            row.append('You must be over 18 to view this page')

        else:
            karma = driver.find_element(By.CLASS_NAME, '_1hNyZSklmcC7R_IfCUcXmZ')
            ActionChains(driver).move_to_element(karma).perform()
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            for value in scraping_user_profile.values():
                scraping_data_by_class(class_str=value, soup=soup)

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    start_datetime = datetime.today().strftime('%Y.%m.%d.%H:%M')
    print(start_datetime)

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        result = parse_hundred_href()
        if result:
            break
        new_height = driver.execute_script("return document.body.scrollHeight")
        last_height = new_height

    for link in link_set:
        scraping(link)
        final_result[len(final_result):] = [list(row)]
        row.clear()

    with open(str(start_datetime) + '.txt', mode='wt', encoding='utf-8') as myfile:
        for row in final_result:
            myfile.write('|'.join(str(item) for item in row))
            myfile.write('\n')
    driver.quit()

    stop_datetime = datetime.today().strftime('%Y.%m.%d.%H:%M')
    print(stop_datetime)