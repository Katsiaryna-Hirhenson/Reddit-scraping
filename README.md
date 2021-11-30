
# iTechArt_StudentLab_Hirhenson
# Reddit Scraping

## Description

Project ‘Reddit Scraping’ parses information from the website https://www.reddit.com.
This program parses month top posts, generates a unique ID for each and gets the following info:
- Link to the post
- Username
- User cake day
- Full karma
- When posted
- Number of comments
- Number of votes
- Category

## How it works?

First the program opens https://www.reddit.com/top/?t=month and collects links for posts.
Next it opens each post, collects necessary information and moves to user profile.
Aftaer collecting information from user profile, it moves to the next post.

When all information for posts is collected, it is sent to http://localhost:8087/.
Usin server module you can interact with this information via POST/GET/PUT/DELETE requests. 
You will find more detailed information on how to use requests further in section "**How to interact with server**"

## What needs to be installed

 - [ ] **Chrome browser**

 Get Chrome browser at https://www.google.com/intl/ru/chrome/
 - [ ] **Chromedriver for your browser version**
 
 
Download a driver for your browser version at https://chromedriver.storage.googleapis.com/index.html
 - [ ] **Python 3**

Get Python 3 at https://www.python.org/downloads/


## How to launch

**NOTE!** The program takes a wile to execute, please be patient and try not to use any other programs simultaneously!

First you need to clone git repository.
Open your terminal and paste the following:

    $git clone https://github.com/Katsiaryna-Hirhenson/iTechArt_StudentLab_Hirhenson.git scraping
This line of code will creat a folder 'scraping' with repository files.

Next you need to move to your project directory.

    $cd scraping

Then you need to launch virtual envirnoment for this project.

    $python3 -m venv scraping_env
And activate it.

    $source -m  scraping_env/bin/activate
Then you need to inall requirements.txt file.

    $python3 -m pip install -r requirements.txt
Now you can move to project files.
First of all you need to run server.py module.

    $python3 server.py

You should see a message like this: Tue Nov 23 15:17:21 2021 Server Starts - localhost:8087

Next step is to launch main.py
**You need to open another window of your terminal. 
SERVER MUST BE STILL RUNNING!**
Here you need to run main.py file, insert number of posts you would like to parse and put in path to your chromedriver. All seperated by spaces.

    $python3 main.py 100 /Users/reddit_scraping/chromedriver


The program should start executing. You will see a message 'Start parsing at ...' .
When all information is collected you will see a message 'Stop parsing at ...' .
Then information will be sent to your local server and you can start interacting with it. 

## How to interact with server

This server module provides responces for POST/GET/PUT/DELETE requests.
It is much more convenient to use **Postman** for interaction.
**You can find it at https://www.postman.com/**

**NOTE!** UNIQUE_ID should be in a format of 32 elemen line of numbers and letters (Latin alphabet, lowercase).

*Example: 5bbdd2544bdb11ecb952acde48001122*

**COMMANDS:**

    POST http://localhost:8087/posts

Receves data and creates a .txt document where one line contains information about one post.

    GET http://localhost:8087/posts

Returns all posts in json format.

    GET http://localhost:8087/posts/UNIQUE_ID

Returns one post with corresponding id in json format.

    DELETE http://localhost:8087/posts/UNIQUE_ID
    
Deletes one post with corresponding id.

    PUT http://localhost:8087/posts/UNIQUE_ID

Updates one post with corresponding id.
The format of line you would like to update should be "UNIQUE ID;new information;".
