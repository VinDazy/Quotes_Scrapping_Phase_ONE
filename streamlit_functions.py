import time
import json
import numpy as np
#import matplotlib.pyplot as plt
import json
from bs4 import BeautifulSoup
import requests
import streamlit as st


def st_scrape(num_pages):
    data = {}
    index_counter = 0
    for i in range(num_pages):
        link = f"https://quotes.toscrape.com/page/{i+1}/"
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'lxml')
        quotes = soup.find_all('div', class_='quote')
        for element in quotes:
            quote = element.find('span', class_='text').text
            tags = element.find_all('a', class_='tag')
            tags = [tag.text for tag in tags]
            author = element.find('small', class_='author').text
            about_link = element.find('a', href=True, string='(about)')['href']

            about_link = 'http://quotes.toscrape.com/' + about_link
            data[index_counter+1] = {
                'quote': quote,
                'author': author,
                'tags': tags,
                'author_bio': about_link
            }
            index_counter += 1
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return data
def st_author_quotes(author_name, data):
    quotes = []
    for quote in data:
        if data[quote]['author'] == author_name:
            quotes.append(data[quote]['quote'])
    if len(quotes) == 0:
        return f'Author : "{author_name}" not found'
    return quotes
def st_unique_authors(data:dict):
    unique_authors = []
    for quote_data in data.values():
        author = quote_data['author']
        if author not in unique_authors:
            unique_authors.append(author)
    return unique_authors
def st_filter_tags(data):
    """takes the data file as input and returns a set of all the unique tags found in the scraped data  """
    tags = set()
    for quote in data:
        tags.update(tuple(data[quote]['tags']))
    return (tags)

def st_tags_quotes(tags, data, number):
    """Takes the data file as input and the tags which are returned from the tags_input function.
    Returns a dictionary of quotes containing similar to exact matching tags."""
    quotes_dict = {}
    count = 0
    for quote in data:
        for tag in data[quote]['tags']:
            if tag in tags:
                quotes_dict[count+1] = {
                    'quote': data[quote]['quote'],
                    'author': data[quote]['author'],
                    'tags': data[quote]['tags'],
                    'Author Bio link': data[quote]['author_bio']
                }
                count += 1
                if count == number:
                    return quotes_dict.values()

    if count == 0:
       st.write("<span style='color:red'>Sorry, we could not find any quotes containing similar tags. Please try different tags.</span>", 
         unsafe_allow_html=True, 
         )

    else:
        st.write(f"<span style='color:red'>Sorry, we could only find {count} quote (s) containing similar tags to which you entered.</span>", 
         unsafe_allow_html=True,)

    return quotes_dict.values()
def author_bio_link(author_name,data):
    for quote in data:
        if author_name==data[quote]['author']:
            return data[quote]['author_bio']
