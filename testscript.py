from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


driver = Chrome(executable_path='/chromedriver')
driver.get('https://www.reddit.com/top/?t=month')


SCROLL_PAUSE_TIME = 10

last_height = driver.execute_script("return document.body.scrollHeight")

link_list = []
while len(link_list) != 100:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    post_urls = driver.find_elements(By.CLASS_NAME, '_3jOxDPIQ0KaOWpzvSQo-1s')
    for post_url in post_urls:
        post_link = post_url.get_attribute('href')
        link_list.append(post_link)
        print(len(link_list))

    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    last_height = new_height

#post_urls = driver.find_elements(By.CLASS_NAME, '_3jOxDPIQ0KaOWpzvSQo-1s')
# actions = ActionChains(driver)
# actions.move_to_element(elem)
# actions.click(elem)
# actions.perform()

