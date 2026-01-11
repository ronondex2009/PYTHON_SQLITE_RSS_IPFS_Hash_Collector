#!/bin/env python3
import requests
from bs4 import BeautifulSoup
import sqlite3
import time

LOOP_INFINITE   = False # Set to true if you are not calling this program via cron or other means
LOOP_WAIT       = 320    # Seconds to wait before update if set to LOOP_INFINITE
DATABASE_PATH   = r"./IPFS_Hashes.db"
RSS_FEED        = r"https://www.reddit.com/r/IPFS_Hashes/.rss"

def fetch_recent_rss_entries():
    """
        Fetches rss feed from selected location (reddit) and
        converts it to the individual entries
    """
    # fetch http request
    reddit_feed_rss = requests.get(RSS_FEED)

    # return if not OK
    if reddit_feed_rss.status_code != 200:
        print("Request did not return OK, no data is pulled.")
        print(reddit_feed_rss.text)
        return []

    # start parsing
    reddit_feed_rss_soup = BeautifulSoup(reddit_feed_rss.content, "xml")
    entries = reddit_feed_rss_soup.feed.find_all("entry")
    return entries

def convert_entry_xml_to_entry_tuple(entry):
    return (
        entry.id.get_text(),
        entry.author.name,
        entry.published.get_text(),
        entry.updated.get_text(),
        entry.title.get_text(),
        entry.content.get_text()
    )

def initialize_table(conn):
    cursor = conn.cursor()
    # table schema
    if cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hashes';").fetchone() == None:
        print("regenerating table schema")
        cursor.execute("""
            CREATE TABLE hashes (
                id VARCHAR(10) PRIMARY KEY,
                author NVARCHAR(23),
                published DATETIME,
                updated DATETIME,
                title TEXT,
                content TEXT
            )
        """)


def write_rss_entries_to_database(conn, entries):
    # parse the entries
    entries_processed = map(convert_entry_xml_to_entry_tuple, entries)
    map(lambda x: print(x), entries_processed)
    cursor = conn.cursor()
    cursor.executemany(
        """ INSERT OR IGNORE INTO hashes (id, author, published, updated, title, content)
            VALUES (?, ?, ?, ?, ?, ?);
        """, entries_processed
        )

if __name__ == "__main__":
    conn = sqlite3.connect(DATABASE_PATH)
    initialize_table(conn)
    while True:
        entries = fetch_recent_rss_entries()
        write_rss_entries_to_database(conn, entries)
        conn.commit()
        if LOOP_INFINITE:
            time.sleep(LOOP_WAIT)
        else:
            break
    print("Finished")
