import sqlite3
import json


with open('data.json', 'r', encoding='utf-8') as json_file:
    # Load the JSON data from the file
    data_dict = json.load(json_file)

class author :
    def __init__(self,author_id,author_name,author_link):
        self.author_id=author_id
        self.author_name=author_name
        self.author_link=author_link
    def __str__(self):
        return f"author_id : {self.author_id}, author_name: {self.author_name}, author_link : {self.author_link}"
class quote :
    def __init__(self,quote,quote_id,author_id):
        self.quote=quote
        self.quote_id=quote_id
        self.author_id=author_id
    def __str__(self) -> str:
         return f"quote_id : {self.quote_id}, author_id : {self.author_id}, quote : {self.quote}"
    
         
def insert_author(author:author):
    with con:
        cursor.execute("INSERT INTO author VALUES (?, ?, ?)",(author.author_id, author.author_name,author.author_link))
def insert_quote(quote:quote):
    with con:
        cursor.execute("INSERT INTO quote VALUES (?, ?, ?)",(quote.quote, quote.quote_id, quote.author_id))


    
def create_author_instances(data_dict):
    author_instances = []
    author_id_counter = 1

    for quote_id, quote_data in data_dict.items():
        author_name = quote_data['author']
        author_link = quote_data['author_bio']

        # Check if the author already exists in the list of author instances
        existing_author = next((author for author in author_instances if author.author_name == author_name), None)

        if existing_author is None:
            # Create a new instance of the Author class for the distinct author
            new_author = author(author_id=author_id_counter, author_name=author_name, author_link=author_link)
            author_instances.append(new_author)
            author_id_counter += 1

    return author_instances


def create_quote_instances(data_dict):
    quote_instances = []
    quote_id_counter = 1
    for quote_id, quote_data in data_dict.items():
        author_name = quote_data['author']

        # Fetch the author_id from the "author" table based on the author_name
        cursor.execute("SELECT author_id FROM author WHERE author_name=?", (author_name,))
        result = cursor.fetchone()

        if result is None:
            # If the author is not found in the "author" table, you can handle it accordingly
            # For now, we'll simply skip this quote
            continue

        author_id = result[0]

        # Create a new instance of the Quote class and add it to the quote_instances list
        new_quote = quote(quote=quote_data['quote'], quote_id=quote_id_counter, author_id=author_id)
        quote_instances.append(new_quote)
        quote_id_counter += 1
    return quote_instances
def fill_tags_table():
    with con : 
        with open("tags.txt",'r') as f :
            tag_id=1
            for word in f :
                word=word.strip()
                cursor.execute("INSERT INTO tags VALUES (?, ?)",(word, tag_id))
                tag_id+=1

def get_tag_id(tag):
    cursor.execute("SELECT tag_id FROM tags WHERE tag=?", (tag,))
    result = cursor.fetchone()
    if result is not None:
        return result[0]
    else:
        return None

# Function to retrieve the quote_id for a given quote from the 'quote' table
def get_quote_id(quote_text):
    cursor.execute("SELECT quote_id FROM quote WHERE quote=?", (quote_text,))
    result = cursor.fetchone()
    if result is not None:
        return result[0]
    else:
        return None


# Iterate through the data_dict and fill the 'tags_quotes' table
def fill_tags_quotes_table(data_dict):
    with con:
        for quote_data in data_dict.values():
            quote_text = quote_data['quote']
            quote_id = get_quote_id(quote_text)

            if quote_id is not None:
                tags = quote_data['tags']
                for tag in tags:
                    tag_id = get_tag_id(tag)

                    if tag_id is not None:
                        cursor.execute("INSERT INTO tags_quotes VALUES (?, ?)", (tag_id, quote_id))










#! for testing purposes, we create our db on ram, then when testing is done, replace :memory: with database.db


con=sqlite3.connect("mydb.db")
cursor=con.cursor()

cursor.execute(
"""
    CREATE TABLE author(
    author_id integer,
    author_name string,
    author_link text
    )
""")
cursor.execute(
"""
    CREATE TABLE quote(
    quote text,
    quote_id integer,
    author_id integer
    )
""")


cursor.execute(
"""
    CREATE TABLE tags(
    tag text,
    tag_id integer
    )
""")


cursor.execute(
"""
    CREATE TABLE tags_quotes(
    tag_id integer,
    quote_id integer
    )
""")
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
for author_instance in create_author_instances(data_dict):
    insert_author(author_instance)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#! at this point we filled our author table with the right data 
#cursor.execute("SELECT author_name FROM author")
#cursor.execute("SELECT author_link FROM author")
#cursor.execute("SELECT author_id FROM author")
#print(cursor.fetchall())



# Print the data of each quote instance
for quote_instance in  create_quote_instances(data_dict):
    insert_quote(quote_instance)
#cursor.execute("SELECT * FROM quote") 
#for item in cursor.fetchall():
    #print (item[1],"\t",item[2],"\t",item[0])


fill_tags_table()
fill_tags_quotes_table(data_dict)   

