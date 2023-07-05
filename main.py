import json
from bs4 import BeautifulSoup
import requests

def scrape():
    pages = int(input("How many pages to scrape?\n>> "))
    data = {}
    for i in range(pages):
        link = f"https://quotes.toscrape.com/page/{i+1}/"
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'lxml')
        quotes = soup.find_all('div', class_='quote')
        for index, element in enumerate(quotes):
            quote = element.find('span', class_='text').text
            tags = element.find_all('a', class_='tag')
            tags = [tag.text for tag in tags]
            tags_str = ', '.join(tags)
            author = element.find('small', class_='author').text
            about_link = element.find('a', href=True, text='(about)')['href']
            about_link = 'http://quotes.toscrape.com/' + about_link
            data[index+1] = {
                'quote': quote,
                'author': author,
                'tags': tags,
                'about_link': about_link
            }
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    scrape()

if __name__ == '__main__':
    main()
