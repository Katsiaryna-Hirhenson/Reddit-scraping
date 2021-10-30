from bs4 import BeautifulSoup
import requests


url = 'https://www.reddit.com/user/hestolemysmile/'
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}

html_data = requests.get(url=url, headers=headers)
soup = BeautifulSoup(html_data.text, 'lxml')

user_name = soup.find(class_='_1LCAhi_8JjayVo7pJ0KIh0')
print(user_name.text)

user_cake_day = soup.find(id='profile--id-card--highlight-tooltip--cakeday')
print(user_cake_day.text)