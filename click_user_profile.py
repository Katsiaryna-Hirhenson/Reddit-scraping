from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time

driver = Chrome(executable_path='/Users/ekaterinagirgenson/Proga/PycharmProjects/reddit_scraping/chromedriver')
driver.get('https://www.reddit.com/r/antiwork/comments/q82vqk/quit_my_job_last_night_it_was_nice_to_be_home_to/')

time.sleep(5)
user_profile = driver.find_element(By.CLASS_NAME, '_2mHuuvyV9doV3zwbZPtIPG')
user_profile.click()