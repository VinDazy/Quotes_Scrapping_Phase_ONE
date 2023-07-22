import time
import json
import numpy as np
import matplotlib.pyplot as plt
import json
from bs4 import BeautifulSoup
import requests
import streamlit as st
from PIL import Image
from io import BytesIO
from functions import *
import plotly.graph_objects as go
import requests
from bs4 import BeautifulSoup
import streamlit as st
from PIL import Image
import io


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
    """using the author_name(string) and the data(dict) as input , this function returns the corresponding bio link of the author of type string """
    for quote in data:
        if author_name==data[quote]['author']:
            return data[quote]['author_bio']



def st_scrape_image(author_name,placement):
    """this function takes the author_name(str) and placement(string) as input, scrapes the corresponding author image in their wikipedia page and displays it in the correct placement in a streamlit web app  """
    author_name = author_name.replace(" ", '_')
    url = "https://en.wikipedia.org/wiki/"
    url = url + author_name

    try:
        # Set the User-Agent header to comply with the Wikimedia User-Agent policy
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Send a GET request to the author's Wikipedia page
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the infobox table on the page
        infobox = soup.find('table', class_='infobox')

        if infobox is not None:
            # Find the first image in the infobox
            image = infobox.find('img')

            if image is not None:
                # Get the source URL of the image
                image_url = image['src']

                # Handle relative and absolute image URLs
                if not image_url.startswith('http'):
                    image_url = 'https:' + image_url

                # Download the image
                response = requests.get(image_url, headers=headers)
                response.raise_for_status()

                # Check if the response content is image data
                content_type = response.headers.get('Content-Type')
                if 'image' in content_type:
                    # Load the image from the response content
                    image_data = response.content
                    image = Image.open(io.BytesIO(image_data))

                    # Display the image in the Streamlit web app
                    placement.image(image)
                else:
                    placement.write('The response does not contain image data.')
            else:
                placement.write('No image found for the author.')
        else:
            placement.write('No infobox found on the Wikipedia page.')

    except requests.exceptions.RequestException as e:
        placement.write(f'An error occurred: {e}')

def st_graph_tag_instance(data):

    """Using the data file as input, this function shows a plot of the top 10 unique tags and their associated number of instances."""
    tag_instances = count_tag_instances(data)
    sorted_tags = sorted(tag_instances.items(), key=lambda x: x[1], reverse=True)
    top_tags = [tag for tag, _ in sorted_tags[:10]]
    top_instances = [tag_instances[tag] for tag in top_tags]

    fig = go.Figure(data=[
        go.Bar(x=top_tags, y=top_instances, marker=dict(color=['red' if instance == max(top_instances) else 'blue' for instance in top_instances]))
    ])

    fig.update_layout(
        title='Top 10 tags',
        xaxis_title='Tags',
        yaxis_title='Instances',
        showlegend=False,
        height=500,
        width=650,
        margin=dict(l=50, r=50, t=50, b=50)
    )

    return(fig)
def st_graph_author_quote(data):
    """
    Graph the authors with their respective numbers of quotes and highlights the maximum
    """
    author_quotes_dict = filter_authors(data)
    sorted_authors = sorted(author_quotes_dict.items(), key=lambda x: x[1]['Nb_quotes'], reverse=True)

    top_authors = [author for author, _ in sorted_authors[:10]]
    top_quotes = [author_quotes_dict[author]['Nb_quotes'] for author in top_authors]

    fig = go.Figure(data=[
        go.Bar(x=top_authors, y=top_quotes, marker=dict(color=['red' if quotes == max(top_quotes) else 'blue' for quotes in top_quotes]))
    ])

    fig.update_layout(
        title=f'Top {len(top_authors)} Authors',
        xaxis_title='Authors',
        yaxis_title='Number of Quotes',
        showlegend=False,
        height=500,
        width=650,
        margin=dict(l=50, r=50, t=50, b=50)
    )

    return fig 