import logging
import uuid
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def main():
    logging.basicConfig(
        filename='logname.log',
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG
    )

    logger = logging.getLogger(__name__)

    final_result = []

    url = 'https://www.reddit.com/top/?t=month'

    driver = webdriver.Chrome(
        executable_path='/Users/ekaterinagirgenson/Proga/PycharmProjects/reddit_scraping/chromedriver')
    driver.implicitly_wait(300)
    driver.get(url)

    last_height = driver.execute_script("return document.body.scrollHeight")
    link_set = set()

    start_datetime = datetime.today().strftime('%Y.%m.%d')
    print(start_datetime)

    logging.info('Start parsing 100 post links')

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

    scraping_post_profile = {'full_date': '_2J_zB4R1FH2EjGMkQjedwc u6HtAZu8_LKL721-EnKuR',
                             'comments': 'FHCV02u6Cp2zYL0fhQPsO',
                             'votes': '_1E9mcoVn4MYnuBQSVDt1gC',
                             'category': '_19bCWnxeTjqzBElWZfIlJb',
                             }

    scraping_user_profile = {'user_cake_day': '_3KNaG9-PoXf4gcuy5_RCVy',
                             'full_karma': '_3uK2I0hi3JFTKnMUFHD2Pd',
                             }

    def scraping_data_by_class(str):
        data = soup.find(class_=str)
        data = data.text
        row.append(data)

    logger.info(u'Start scraping info')
    for link in link_set:
        row = []
        driver.get(link)
        logger.info('Open each post and scrape date, comments, votes, category, author, link to author profile')
        uid = uuid.uuid1().hex
        row.append(uid)
        date_posted = driver.find_element(By.CLASS_NAME, '_3jOxDPIQ0KaOWpzvSQo-1s')
        ActionChains(driver).move_to_element(date_posted).perform()
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        for value in scraping_post_profile.values():
            scraping_data_by_class(value)

        # get link to move to user profile
        user_profile = soup.find(class_='_2mHuuvyV9doV3zwbZPtIPG')
        user_a = user_profile.find('a')
        user_url_name = user_a['href']
        row.append(user_url_name)
        user_url = 'https://www.reddit.com' + str(user_url_name)

        logger.info('Move to user profile, scrape karma and cake day')
        driver.get(user_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        # check if you are on "are you over 18" page; if yes, skip this post
        if soup.find(class_='bDDEX4BSkswHAG_45VkFB'):
            continue

        karma = driver.find_element(By.CLASS_NAME, '_1hNyZSklmcC7R_IfCUcXmZ')
        ActionChains(driver).move_to_element(karma).perform()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_3uK2I0hi3JFTKnMUFHD2Pd')))
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        for value in scraping_user_profile.values():
            scraping_data_by_class(value)

        final_result.append(row)

    with open(str(start_datetime) + '.txt', mode='wt', encoding='utf-8') as myfile:
        for row in final_result:
            myfile.write('|'.join(str(item) for item in row))
            myfile.write('\n')

    driver.quit()
    stop_datetime = datetime.today().strftime('%Y.%m.%d.%H:%M')
    print(stop_datetime)


if __name__ == '__main__':
    main()