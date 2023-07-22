import requests
from bs4 import BeautifulSoup
import os
"""
this function takes in an author name as input, scrapes their corresponding wikipedia image and saves it in a "Author Pictures" directory 
"""


def scrape_image(author_name):
    author_name = author_name.replace(" ", '_')
    url = "https://en.wikipedia.org/wiki/"
    url = url + author_name

    # Create a directory to store the images
    directory = 'Author Pictures'
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        # Send a GET request to the author's Wikipedia page
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
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

                # Save the image with the author's name as the file name
                image_name = f'{directory}/{author_name}.jpg'
                with open(image_name, 'wb') as file:
                    file.write(response.content)

                print(f'Saved image: {image_name}')
            else:
                print('No image found for the author.')
        else:
            print('No infobox found on the Wikipedia page.')

    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')


