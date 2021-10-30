from bs4 import BeautifulSoup
import requests


url = 'https://www.reddit.com/r/antiwork/comments/q82vqk/quit_my_job_last_night_it_was_nice_to_be_home_to/'
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}

html_data = requests.get(url=url, headers=headers)
soup = BeautifulSoup(html_data.text, 'lxml')

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