# iTechArt_StudentLab_Hirhenson
# Reddit Scraping

## Description

Project ‘Reddit Scraping’ parses information from the website https://www.reddit.com.
This program parses month top 100 posts, generates a unique ID for each and gets the following info:
- Link to the post
- Username
- User cake day
- Full karma
- When posted
- Number of comments
- Number of votes
- Category

## How it works?

First the program opens https://www.reddit.com/top/?t=month and collects links for 100 posts.
Next it opens each post, collects necessary information and moves to user profile.
Aftaer collecting information from user profile, it moves to the next post.

When all information for 100 posts is collected, it is sent to http://localhost:8087/.
Usin server module you can interact with this information via POST/GET/PUT/DELETE requests. 
You will find more detailed information on how to use requests further in section "**How to interact with server**"

## What needs to be installed

- Chrome browser
- Chromedriver for your browser version
- Python 3
- Requirements.txt

Get Chrome browser at https://www.google.com/intl/ru/chrome/

Chromedriver is needed for the script to be able to interact with your Chrome browser
Download a driver for your browser version at https://chromedriver.storage.googleapis.com/index.html

Get Python 3 at https://www.python.org/downloads/

“Requirements files” are files containing a list of items to be installed in this project
To install it use:
For Unix\macOs: python -m pip install -r requirements.txt
For Windows: py -m pip install -r requirements.txt

## How to launch

**NOTE!** The program takes a wile to execute, please be patient and try not to use any other programs simultaneously!

First of all you need to run server.py module.
You need to open a command-line of your terminal and type the word python3 followed by the path to your server.py file.
Examples: python3 /Users/reddit_scraping/server.py

You should see a message like this: Tue Nov 23 15:17:21 2021 Server Starts - localhost:8087

Next step is to launch main.py
You need to open another window of your terminal. SERVER MUST BE STILL RUNNING!
Here you will be passing two paths, one to your main.py file and another one to your chromedriver.
Type the word python3 followed by the path to your main.py file, than press spase and insert path to your chromedriver
Examples: python3 /Users/reddit_scraping/main.py /Users/reddit_scraping/chromedriver

The program should start executing. You will see message 'Start parsing at "current date and time "'.
When all information is collected you will see message 'Stop parsing at "current date and time "'.
Then information will be sent to your loval server and you can start interacting with it. 

## How to interact with server

This server module provides responces for POST/GET/PUT/DELETE requests.
It is much more convenient to use Postman for interaction.
You can find it at https://www.postman.com/

**NOTE!** UNIQUE ID should be in a format of 32 elemen line of numbers and letters (Latin alphabet, lowercase). Example: 5bbdd2544bdb11ecb952acde48001122

**POST http://localhost:8087/**

Receives data and writes it into txt file. 
File will have following name: reddit-CURRENT_DATE.txt, where CURRENT_DATE is today's date in "year.month.day.hours.minutes" format.

**POST http://localhost:8087/posts**

Adds new line to a document.
The format of new line should be "UNIQUE ID: [new informatiom]".

**GET http://localhost:8087/posts**

Returns all posts in json format.

**GET http://localhost:8087/posts/UNIQUE ID**

Returns one post with corresponding id in json format.

**DELETE http://localhost:8087/posts/UNIQUE ID**

Deletes one post with corresponding id.

**PUT http://localhost:8087/posts/UNIQUE ID**

Updates one post with corresponding id.
The format of line you would like to update should be "UNIQUE ID: [new information]".
