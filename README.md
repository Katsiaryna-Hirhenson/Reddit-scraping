# iTechArt_StudentLab_Hirhenson

Project ‘Reddit Scraping’ meant to parse information from the website https://www.reddit.com
This program covers top 100 post over the month, generates a unique ID for each and gets the following info:
- Link to the post
- Username
- User cake day
- Full karma
- When posted
- Number of comments
- Number of votes
- Category

To execute code you need to use 'main.py' file
Scraped information is stored in a file with a current date and time in a .txt format
The program takes a wile to execute, please be patient and try not to use any other programs simultaneously

To make the program work you need:
- Use Chrome browser
- Download a driver for your browser version at https://chromedriver.storage.googleapis.com/index.html
- Open 'main.py'
- Copy an executable path to your driver and paste it into a ‘driver = webdriver.Chrome(executable_path='') ’variable in the project
-  “Requirements files” are files containing a list of items to be installed in this project
To install it use:
For Unix\macOs: python -m pip install -r requirements.txt
For Windows: py -m pip install -r requirements.txt
