# -*- coding: utf-8 -*-

"""
change:
in DATABASE_PROXY = {
    '--username--',
    '--pass--',
    '--dbname--',

and in SETTINGS = {
    '--url to your-script php---',
    '--your IP--',
and rename from 'creds_pattern.py' to 'creds.py'
"""

my_local_host = 'localhost'
my_local_mysql_port = 3306


DATABASE_PROXY = {
    'drivername': 'mysql',
    'host': my_local_host,
    'port': my_local_mysql_port,
    'username': '--username--',
    'password': '--pass--',
    'database': '--dbname--',
}


SETTINGS = {
    'url_ip': '--url to your-script php---',
    'look_for_ip': '--your IP--',
}