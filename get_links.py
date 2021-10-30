from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


# if __name__ == '__main__':
driver = Chrome(executable_path='/chromedriver')
driver.get('https://www.reddit.com/top/?t=month')

SCROLL_PAUSE_TIME = 1

last_height = driver.execute_script("return document.body.scrollHeight")
link_list = []


def parse_hundred_href():
    post_urls = driver.find_elements(By.CLASS_NAME, '_3jOxDPIQ0KaOWpzvSQo-1s')
    for post_url in post_urls:
        post_link = post_url.get_attribute('href')
        if len(link_list) >= 100:
            return True

        link_list.append(post_link)
    time.sleep(SCROLL_PAUSE_TIME)


while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    result = parse_hundred_href()
    if result:
        break
    new_height = driver.execute_script("return document.body.scrollHeight")
    last_height = new_height


for link in link_list:
    print(link, '\n')
