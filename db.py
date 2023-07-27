import json
import sqlite3 
con=sqlite3.connect("database.db")
cursor=con.cursor()

#cursor.execute(
#"""
#    CREATE TABLE author(
#    author_id integer,
#    author_name string,
#    author_link text
#    )
#""")


#cursor.execute(
#"""
#    CREATE TABLE quote(
#    quote text,
#    quote_id integer,
#    author_id integer
#    )
#""")


#cursor.execute(
#"""
#    CREATE TABLE tags(
#    tag text,
#    tag_id integer
#    )
#""")


#cursor.execute(
#"""
#    CREATE TABLE tags_quotes(
#    tag_id integer,
#    quote_id integer
#    )
#""")
cursor.execute("INSERT INTO author VALUES (123, 'Albert Einstein', 'http://quotes.toscrape.com//author/Albert-Einstein')")
con.commit()
print(cursor.fetchall())


con.commit()

con.close()