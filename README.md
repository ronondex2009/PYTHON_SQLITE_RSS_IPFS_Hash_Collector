# PYTHON_SQLITE_RSS_IPFS_Hash_Collector
Python script that fetches IPFS hashes from a reddit RSS feed and collects them into an SQLite database. By default, configured to parse and collect from https://www.reddit.com/r/IPFS_Hashes/.rss

## DEPENDENCIES
python python-requests python-lxml python-sqlite3 python-beautifulsoup4

## SETUP
It is recommended to setup a crontab to run this program every 5 or longer minutes, or enable the program to run on a loop with the global variable in the python script and start it manually.
The script will be blocked by the servers if it is set to request the rss feed too frequently. Please set the loop length to a reasonable value.

The database file need not be the one included in this repository. The script will automatically setup table schemas for `hashes` and `posts` if they do not already exist. It is recommended to use an SQLite database.

## USAGE
The script may not always find the hash in the content. Posts may not always contain the hash.
Hashes are stored in a table called `hashes`, where IDs may not be unique (in the case of a post having several hashes included)
The script can also theoretically work on other reddit feeds. You can also use it to collect posts from non-IPFS-hash reddits, and just use the `posts` table.
