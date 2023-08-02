import requests
from bs4 import BeautifulSoup
import streamlit as st
from PIL import Image
from io import BytesIO
"""
this function takes in an author name as input , scrapes their corresponding wikipedia image and displays it into a streamlit web app 
"""


def scrape_image(author_name):
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

                # Load the image from the response content
                img = Image.open(BytesIO(response.content))

                # Display the image in the Streamlit web app
                st.image(img)
            else:
                st.write('No image found for the author.')
        else:
            st.write('No infobox found on the Wikipedia page.')

    except requests.exceptions.RequestException as e:
        st.write(f'An error occurred: {e}')


# Create the Streamlit web app
def main():
    st.title("Author Image Scraper")

    # Input field for author name
    author_name = st.text_input("Enter the author name")

    # Scrape and display the image
    if st.button("Scrape Image"):
        scrape_image(author_name)


if __name__ == '__main__':
    main()
