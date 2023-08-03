import time
import json
import numpy as np
import matplotlib.pyplot as plt
import json
from bs4 import BeautifulSoup
import requests


def scrape():
    """
    this function takes a number of pages to scrape as input (keeping in mind that the maximum number of pages is 10), scrapes the quote,author,tags and author's bio link and stores them in a dictionnary, then converts all the data to a json file called data.json 
    """
    reply = str(
        input("Do you want to scrape all the website content? \n>>(Y/N) : "))
    if reply.upper() == 'Y':
        pages = 10
    else:
        pages = int(input("How many pages to scrape?(<=9)\n>> "))
        while pages not in range(1, 10):
            pages = int(input("How many pages to scrape?(<=9)\n>> "))
    data = {}
    index_counter = 0
    for i in range(pages):
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
                'about_link': about_link
            }
            index_counter += 1
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return data


#! 1 . implement the search functions , given a data dictionnary and an author's full name as input, ouput all the quotes written by this author


def name_input():
    """
    takes input for an authors name as a string and returns it 
    """
    author_name = str(input("Enter Author name : \n>> "))
    return author_name


def author_quotes(author_name, data):
    """
    takes the data file (data : dict) as input and the author's name from the name_input functions and returns a list of all the quotes' associated to that author 
    """
    quotes = []
    for quote in data:
        if data[quote]['author'] == author_name:
            quotes.append(data[quote]['quote'])
    if len(quotes) == 0:
        return f'Author : "{author_name}" not found'
    return quotes


# print(author_quotes(author_name=name_input(),data=scrape()))
"""---------------------------------------------------------------------------------------------------------------------------"""
#! 2 . implement the recommendation system ; for this to work :
# ? - extract all the tags for the user to pick from     ✔
# * - this is exactly why you need to comment your code, for a second i thought extracting all the tags would be useless, until i read the comment, thank you me
# ? - output quote(s) containing similar to exact matching tags ✔
def filter_unique_authors(data):
    unique_authors = []
    for quote_data in data.values():
        author = quote_data['author']
        if author not in unique_authors:
            unique_authors.append(author)
    return unique_authors



def filter_tags(data):
    """takes the data(dict) file as input and returns a set of all the unique tags found in the scraped data  """
    tags = set()
    for quote in data:
        tags.update(tuple(data[quote]['tags']))
    return (tags)
# print(filter_tags(data=scrape()))


def tags_input(data):
    """takes the data (dict) file as input and returns a list of all user input tags """
    print("You may choose your tag(s) from here\n", filter_tags(data))
    tags = (input(
        "Enter the tag(s) you want your quotes to have (Tags must be space-seperated): \n>> "))
    tags = tags.split()
    return tags


def number_quotes():
    """returns the number of quotes to show as integer"""
    number = int(input("Enter number of quotes to ouput : \n>> "))
    return number


def tags_quotes(tags, data):
    """takes the data (dict)  as input and the tags (list) which are returned from the tags_input function , returns a dictionnary of the quotes containing similar to exact matching tags  """
    quotes_dict = {}
    number = number_quotes()
    count = 0
    for quote in data:
        for tag in data[quote]['tags']:
            if tag in tags:
                quotes_dict[count+1] = {
                    'quote': data[quote]['quote'],
                    'author': data[quote]['author'],
                    'tags': data[quote]['tags'],
                    'about_link': data[quote]['about_link']
                }
                count += 1
                if count == number:
                    return quotes_dict

    print(
        f"Sorry we could only find {count} quotes containing similar tags to which you entered . Here are the results\n")
    return quotes_dict


# print(json.dumps(tags_quotes(tags_input(data),data),indent=4,ensure_ascii=False))
"""---------------------------------------------------------------------------------------------------------------------------"""
#! 3.   implement the analyze function ; this function should be able to draw a chart using all the tags as X axis and map their number of instances in the Y axis
#! 3.1. THIS IS OPTIONAL , add an input functionality to highlight a specific tag in the graph


def count_tag_instances(data : dict) :
    """returns a dictionnary of unique tags as keys, and an associated number of instances as values using the data dict as input """
    tag_inst_dict = {key: 0 for key in filter_tags(data)}
    for quote_data in data.values():
        tags = quote_data['tags']
        for tag in tags:
            tag_inst_dict[tag] += 1
    return tag_inst_dict
# print(json.dumps(count_tag_instances(data=data),indent=4,ensure_ascii=False))


def graph_tag_instance(data:dict):
    """using the data dict as input, this functions displays a plot of the top 10 unique tags and their associated number of instances"""
    tag_instances = count_tag_instances(data)
    sorted_tags = sorted(tag_instances.items(),
                         key=lambda x: x[1], reverse=True)
    top_tags = [tag for tag, _ in sorted_tags[:10]]
    top_instances = [tag_instances[tag] for tag in top_tags]
    fig, ax = plt.subplots(figsize=(12, 8))
    bar_width = 0.4
    bar_spacing = 20
    max_instance = max(top_instances)
    colors = ['blue' if instance ==
              max_instance else 'red' for instance in top_instances]
    ax.bar(range(len(top_tags)), top_instances, width=bar_width, color=colors)
    ax.set_xticks(range(len(top_tags)))
    ax.set_xticklabels(top_tags, ha='center')
    ax.set_xlabel('Top 10 Tags')
    ax.set_ylabel('Instances')
    ax.set_title('Number of Instances per Tag')
    plt.subplots_adjust(bottom=0.326, top=0.914, right=0.995, left=0.036)
    plt.show()


def filter_authors(data):
    """takes the data file as input, and returns a dictionnary of authors' names as keys and their associated number of quotes as values """
    author_number_quotes = {}
    for quote_id, quote_info in data.items():
        author = quote_info['author']
        if author not in author_number_quotes:
            author_number_quotes[author] = {'Nb_quotes': 1}
        else:
            author_number_quotes[author]['Nb_quotes'] += 1
    return author_number_quotes
# print(json.dumps(filter_authors(data), indent=4, ensure_ascii=False))


def graph_author_quote(data):
    """
    Graph the authors with their respective numbers of quotes and highlights the maximum using the data dict
    """
    author_quotes_dict = filter_authors(data)
    sorted_authors = sorted(author_quotes_dict.items(),
                            key=lambda x: x[1]['Nb_quotes'], reverse=True)

    top_authors = [author for author, _ in sorted_authors[:10]]
    top_quotes = [author_quotes_dict[author]['Nb_quotes']
                  for author in top_authors]
    fig, ax = plt.subplots(figsize=(17, 8))
    bar_width = 0.4
    bar_spacing = 20
    max_quotes = max(top_quotes)
    colors = ['blue' if quotes ==
              max_quotes else 'red' for quotes in top_quotes]
    ax.bar(range(len(top_authors)), top_quotes, width=bar_width, color=colors)
    ax.set_xticks(range(len(top_authors)))
    ax.set_xticklabels(top_authors, ha='center')
    number_authors = len(top_authors)
    ax.set_xlabel("Authors ")
    ax.set_ylabel('Number of Quotes')
    ax.set_title(f'Top {number_authors} Authors')
    plt.subplots_adjust(bottom=0.057, top=0.914, right=0.995, left=0.048)
    plt.show()


def scrape_data():
    """calculates the run time of the scrape function"""
    start = time.time()
    print("Scraping starting ...\n")
    data = scrape()
    end = time.time()-start
    print("\nScrapping ended\n")
    print(f"Execution time : {round(end,2)} seconds")
    return data



