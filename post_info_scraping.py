from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests

driver = Chrome(executable_path='/Users/ekaterinagirgenson/Proga/PycharmProjects/reddit_scraping/chromedriver')
driver.get('https://www.reddit.com/top/?t=month')

last_height = driver.execute_script("return document.body.scrollHeight")
link_list = []


def parse_hundred_href():
    post_urls = driver.find_elements(By.CLASS_NAME, '_3jOxDPIQ0KaOWpzvSQo-1s')
    for post_url in post_urls:
        post_link = post_url.get_attribute('href')
        if len(link_list) >= 100:
            return True

        link_list.append(post_link)


while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    result = parse_hundred_href()
    if result:
        break
    new_height = driver.execute_script("return document.body.scrollHeight")
    last_height = new_height

count = 1
for link in link_list:
    url = link

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }

    html_data = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(html_data.text, 'lxml')

    print('---------- post ' + str(count))

    content = soup.find(class_='_eYtD2XCVieq6emjKBH3m')
    print(content.text)

    comments = soup.find(class_='FHCV02u6Cp2zYL0fhQPsO')
    print(comments.text)

    votes = soup.find(class_='_1E9mcoVn4MYnuBQSVDt1gC')
    print(votes.text)

    category = soup.find(class_='_19bCWnxeTjqzBElWZfIlJb')
    print(category.text)

    when_posted = soup.find(class_='_3jOxDPIQ0KaOWpzvSQo-1s')
    print(when_posted.text)

    count += 1