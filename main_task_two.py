import json
import logging
import uuid
import time
import requests

from datetime import datetime
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

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

driver = webdriver.Chrome(executable_path='', options=chrome_options)
driver.implicitly_wait(300)
driver.get(url)

last_height = driver.execute_script('return document.body.scrollHeight')
link_set = set()
row = {}
final_result = []
strings = []
UNIQUE_ID = '32a8e6de47de11ecb81facde48001122'

# server functions ----------------------------------------------------------------------------------------------------
def post_new_line(UNIQUE_ID):
    for row in final_result:
        if UNIQUE_ID not in row.keys():
            new_row = {}
            new_row[UNIQUE_ID] = []
            final_result.append(new_row)
            json_add_new_line = json.dumps(new_row, indent=4)
    response = requests.post('http://localhost:8087/posts', data=json_add_new_line)
    return response.json()


def delete_line(UNIQUE_ID):
    for row in final_result:
        if row.keys() == UNIQUE_ID:
            message = 'This post is deleted'
            response = requests.delete('http://localhost:8087/' + UNIQUE_ID, data=message)
            return response.text


def update_line(UNIQUE_ID):
    for row in final_result:
        if row.keys() == UNIQUE_ID:
            row[UNIQUE_ID] = ['Put new data here']
            one_element = {}
            one_element[UNIQUE_ID] = row[UNIQUE_ID]
            json_one_element = json.dumps(one_element, indent=4)
            response = requests.put('http://localhost:8087/' + UNIQUE_ID, data=json_one_element)
            return response


# parsing functions ----------------------------------------------------------------------------------------------------
# + variables

def parse_hundred_href():
    post_urls = driver.find_elements(By.CLASS_NAME, '_3jOxDPIQ0KaOWpzvSQo-1s')
    for post_url in post_urls:
        post_link = post_url.get_attribute('href')
        if len(link_set) >= 100:
            return True

        link_set.add(post_link)


def scraping_data_by_class(class_str, soup, uid):
    data = soup.find(class_=class_str)
    data = data.text
    row[uid].append(data)


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
        row[uid] = []
        date_posted = driver.find_element(By.CLASS_NAME, '_3jOxDPIQ0KaOWpzvSQo-1s')
        ActionChains(driver).move_to_element(date_posted).perform()
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        for value in scraping_post_profile.values():
            scraping_data_by_class(class_str=value, soup=soup, uid=uid)

        # get link to move to user profile
        user_profile = soup.find(class_='_2mHuuvyV9doV3zwbZPtIPG')
        user_a = user_profile.find('a')
        user_url_name = user_a['href']
        row[uid].append(user_url_name)
        user_url = 'https://www.reddit.com' + str(user_url_name)

        driver.get(user_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        # check if you are on "are you over 18" page; if yes, skip this post
        if soup.find(class_='bDDEX4BSkswHAG_45VkFB'):
            row[uid].append('You must be over 18 to view this page')

        else:
            karma = driver.find_element(By.CLASS_NAME, '_1hNyZSklmcC7R_IfCUcXmZ')
            ActionChains(driver).move_to_element(karma).perform()
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            for value in scraping_user_profile.values():
                scraping_data_by_class(class_str=value, soup=soup, uid=uid)

    except Exception as ex:
        print(ex)

# main code ----------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    start_datetime = datetime.today().strftime('%Y.%m.%d.%H:%M')
    print('start parsing at: ', start_datetime)

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        result = parse_hundred_href()
        if result:
            break
        new_height = driver.execute_script("return document.body.scrollHeight")
        last_height = new_height

    for link in link_set:
        scraping(link)
        final_result[len(final_result):] = [dict(row)]
        row.clear()

# script to create .txt document

    # with open('reddit-' + str(start_datetime) + '.txt', mode='wt', encoding='utf-8') as myfile:
    #     for row in final_result:
    #         for key, value in row.items():
    #             myfile.write('{}: {}\n'.format(key, value))

    driver.quit()
    stop_datetime = datetime.today().strftime('%Y.%m.%d.%H:%M')
    print('stop parsing at: ', stop_datetime)

# server script ----------------------------------------------------------------------------------------------------

    hostName = "localhost"
    hostPort = 8087


    class MyServer(BaseHTTPRequestHandler):
        def do_GET (self):
            if self.path.endswith('/'):
                self.send_response(200)
                self.send_header("Content-type","text/html")
                self.end_headers()
                output = ''
                output += '<html><body>'
                for row in final_result:
                    for key, value in row.items():
                        output += ('{}: {}'.format(key, value))
                        output += '</br>'
                output += '</body></html>'
                self.wfile.write(output.encode())
                with open('reddit-' + str(start_datetime) + '.txt', mode='wt', encoding='utf-8') as myfile:
                    for row in final_result:
                        for key, value in row.items():
                            myfile.write('{}: {}\n'.format(key, value))

            if self.path.endswith('/posts'):
                self.send_response(200)
                self.send_header("Content-type", "text/json")
                self.end_headers()
                json_data = json.dumps(final_result, indent=4)
                self.wfile.write(json_data.encode())

            if self.path.endswith('/posts/' + UNIQUE_ID):
                for row in final_result:
                    if UNIQUE_ID in row.keys():
                        self.send_response(200)
                        self.send_header("Content-type", "text/json")
                        self.end_headers()
                        one_element = {}
                        one_element[UNIQUE_ID] = row[UNIQUE_ID]
                        json_one_element = json.dumps(one_element, indent=4)
                        self.wfile.write(json_one_element.encode())
                        break
                    else:
                        self.send_error(404, 'File Not Found: %s' % self.path)


    myServer = HTTPServer((hostName,hostPort),MyServer)
    print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))