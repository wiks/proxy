# proxy
##### Python smal-tool to test free proxies
- Required **Python 2.7** and requirements.txt:
  - beautifulsoup4==4.6.0
  - bs4==0.0.1
  - lxml==4.2.1
  - MySQL-python==1.2.5
  - SQLAlchemy==1.2.7
- License: MIT

Using data from DataBase checking proxies sending request to own page and observe what was returned. Looking in returned content for own IP to state if proxy hide IP or not. 

Repo contain folders 'php' - with files of mini-web showing phps SERVER data, 'python' - with main script "__init__.py" and file 'wiks_proxy.sql' - exported from PHPAdmin structure of DB.

Simply define data in "creds_pattern.py", rename it to "creds.py", and run like: "python __init__.py". Of course list proxies to check (in table 'all' of DB) coudn't be empty :-)
