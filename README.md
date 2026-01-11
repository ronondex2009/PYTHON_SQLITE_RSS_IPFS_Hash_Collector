# PYTHON_SQLITE_RSS_IPFS_Hash_Collector
Python script that fetches IPFS hashes from a reddit RSS feed and collects them into an SQLite database. By default, configured to parse and collect from https://www.reddit.com/r/IPFS_Hashes/.rss

## DEPENDENCIES
python python-requests python-lxml python-sqlite3 python-beautifulsoup4

## USAGE
It is recommended to setup a crontab to run this program every 5 or longer minutes, or enable the program to run on a loop with the global variable in the python script and start it manually.
The script will be blocked by the servers if it is set to request the rss feed too frequently.

The script may not always find the hash in the content.
