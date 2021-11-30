"""This module does parsing of 100 top month posts from Reddit

First code opens URL, scrolls page down until it gets 100 post urls.
Then it opens each link, collects data from the post and moves to user profile.
When all data for 100 posts is parsed, it is sent to http://localhost:8087/.
"""

import logging
import uuid
from datetime import datetime
import argparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


URL = 'https://www.reddit.com/top/?t=month'
USER_URL_PART_ONE = 'https://www.reddit.com'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('window-size=1200x600')
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument("--headless")

parser = argparse.ArgumentParser(description='Number pf posts and path to chromedriver')
parser.add_argument('posts_number', type=int, help='Input number of posts you want to parse')
parser.add_argument('chromedriver_path', type=str, help='Input path to your chromedriver')
args = parser.parse_args()

driver = webdriver.Chrome(executable_path=str(args.chromedriver_path), options=chrome_options)
driver.implicitly_wait(300)
driver.get(URL)

LAST_HEIGHT = driver.execute_script('return document.body.scrollHeight')


SCRAPING_POST_PROFILE = {'full_date': '_2J_zB4R1FH2EjGMkQjedwc u6HtAZu8_LKL721-EnKuR',
                         'comments': 'FHCV02u6Cp2zYL0fhQPsO',
                         'votes': '_1E9mcoVn4MYnuBQSVDt1gC',
                         'category': '_19bCWnxeTjqzBElWZfIlJb'}

SCRAPING_USER_PROFILE = {'user_cake_day': '_3KNaG9-PoXf4gcuy5_RCVy',
                         'full_karma': '_3uK2I0hi3JFTKnMUFHD2Pd'}

LINK_SET = set()
SINGLE_POST = []

logging.basicConfig(filename='logname.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


def parse_hundred_href():
    """Gets 100 post urls."""
    logging.info('Scraping 100 links...\n')
    try:
        post_urls = driver.find_elements(By.CLASS_NAME, '_3jOxDPIQ0KaOWpzvSQo-1s')
        for each_url in post_urls:
            post_url = each_url.get_attribute('href')
            if len(LINK_SET) >= args.posts_number:
                return True
            LINK_SET.add(post_url)

    except TimeoutError as ex:
        logging.exception(ex)


def scraping_data_by_class(class_name: str, soup: str):
    """Collects data by class names.

    :param class_name: used to find and parse data from HTML
    :type class_name: str
    :param soup: HTML page to search through
    :type soup: str
    """
    data = soup.find(class_=class_name)
    data = data.text
    SINGLE_POST.append(str(data) + ';')


def scraping_user_profile(url: str):
    """Opens user profile. Collects user information.

    :param url: user url
    :type url: str
    """
    logging.info('Start scraping user information...\n')
    try:
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        """check if you are on "are you over 18" page; if yes, skip this post"""

        if soup.find(class_='bDDEX4BSkswHAG_45VkFB'):
            yes_button = driver.find_element(By.XPATH,
                                             '//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[2]/div/div/div[1]/div/div/div[2]/button')
            ActionChains(driver).move_to_element(yes_button).click().perform()

        karma = driver.find_element(By.CLASS_NAME, '_1hNyZSklmcC7R_IfCUcXmZ')
        ActionChains(driver).move_to_element(karma).perform()
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        for value in SCRAPING_USER_PROFILE.values():
            scraping_data_by_class(class_name=value, soup=soup)

    except TimeoutError as ex:
        logging.exception(ex)


def scraping_post_information(url: str):
    """Opens post page. Collects information and creates url to user profile.

    :param url: post url
    :type url: str
    """
    logging.info('Start scraping post information...\n')
    try:
        driver.get(url)
        uid = uuid.uuid1().hex
        SINGLE_POST.append(str(uid) + ';')
        SINGLE_POST.append(str(url) + ';')
        date_posted = driver.find_element(By.CLASS_NAME, '_3jOxDPIQ0KaOWpzvSQo-1s')
        ActionChains(driver).move_to_element(date_posted).perform()
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        for value in SCRAPING_POST_PROFILE.values():
            scraping_data_by_class(class_name=value, soup=soup)

        """get link to move to user profile"""

        user_profile = soup.find(class_='_2mHuuvyV9doV3zwbZPtIPG')
        a_tag = user_profile.find('a')
        user_url_name = a_tag['href']
        SINGLE_POST.append(str(user_url_name) + ';')
        user_url = USER_URL_PART_ONE + str(user_url_name)
        scraping_user_profile(user_url)

    except TimeoutError as ex:
        logging.exception(ex)


if __name__ == '__main__':

    start_datetime = datetime.today().strftime('%Y.%m.%d.%H.%M')
    print('Start parsing at ', start_datetime)

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        result = parse_hundred_href()
        if result:
            break
        new_height = driver.execute_script("return document.body.scrollHeight")
        LAST_HEIGHT = new_height

    for link in LINK_SET:
        scraping_post_information(link)

        without_n_string = ''
        for element in SINGLE_POST:
            without_n = element.replace('\n', ';')
            without_n_string += without_n
        without_n_string += '\n'
        logging.info('Posting information on server...\n')
        r = requests.post('http://localhost:8087/posts/', data=without_n_string)
        SINGLE_POST.clear()

    driver.quit()
    stop_datetime = datetime.today().strftime('%Y.%m.%d.%H.%M')
    print('Stop parsing at ', stop_datetime)





