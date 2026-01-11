#!/usr/bin/python3
import sqlite3

DB_PATH = input("What is the path to the databse? Default: ./IPFS_Hashes.db")
if len(DB_PATH) == 0:
    DB_PATH = "./IPFS_Hashes.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

OPTION = ''
while OPTION != 'R' and OPTION != 'P' and OPTION != 'S':
    OPTION = input("What do you want to do?\n[R]eset Database, [P]rint Entries, [S]earch Name\n")
    OPTION = OPTION[0]

if OPTION == 'R':
    input("You are about to delete all data from both tables. This cannot be undone.\nPress any key to continue... ")
    cursor.execute("DROP TABLE hashes")
    cursor.execute("DROP TABLE posts;")
    conn.commit()
if OPTION == 'P':
    cursor.execute("SELECT posts.id, hash, title, author, published, updated, content FROM posts JOIN hashes ON posts.id = hashes.id;")
    print(f"{'id':<12}{'hash':<48}{'title':<50}{'author':<25}{'published':<16}{'updated':<16}{'content':<64}")
    for x in cursor.fetchall():
        print(f"{x[0]:<12}{x[1]:<48}{x[2]:<50}{x[3]:<25}{x[4]:<16}{x[5]:<16}{x[6]:<64}")
if OPTION == 'S':
    srch = input("SEARCH > ")
    cursor.execute(f"""
        SELECT posts.id, hash, title, author, published, updated, content FROM posts JOIN hashes ON posts.id = hashes.id
        WHERE hash LIKE "%{srch}%"
        OR title LIKE "%{srch}%"
        OR author LIKE "%{srch}%"
        OR published LIKE "%{srch}%"
        OR content LIKE "%{srch}%"
        OR posts.id LIKE "%{srch}%"
    """,
    )
    print(f"{'id':<12}{'hash':<48}{'title':<50}{'author':<25}{'published':<16}{'updated':<16}{'content':<64}")
    for x in cursor.fetchall():
        print(f"{x[0]:<12}{x[1]:<48}{x[2]:<50}{x[3]:<25}{x[4]:<16}{x[5]:<16}{x[6]:<64}")
input()
