
import json
import numpy as np
import matplotlib.pyplot as plt
import json
from bs4 import BeautifulSoup
import requests

def scrape():
    reply=str(input("Do you want to scrape all the website content? \n>>(Y/N) : "))
    if reply.upper()=='Y' :
        pages=10
    else:
        pages = int(input("How many pages to scrape?(<=9)\n>> "))
        while pages not in range (1,10):
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
data =scrape()

#! 1 . implement the search functions , given a data dictionnary and an author's full name as input, ouput all the quotes written by this author 

def name_input():
    author_name=str(input("Enter Author name : \n>> "))
    return author_name

def author_quotes(author_name,data):
    quotes=[]
    for quote in data:
        if data[quote]['author']==author_name:
            quotes.append(data[quote]['quote'])
    if len(quotes)==0:
        return f'Author : "{author_name}" not found'
    return quotes

#print(author_quotes(author_name=name_input(),data=scrape()))
"""---------------------------------------------------------------------------------------------------------------------------"""
#! 2 . implement the recommendation system ; for this to work : 
    #? - extract all the tags for the user to pick from     ✔
    #* - this is exactly why you need to comment your code, for a second i thought extracting all the tags would be useless, until i read the comment, thank you me 
    #? - output quote(s) containing similar to exact matching tags ✔

def scrape_tags(data):
    tags=set()
    for quote in data:
        tags.update(tuple(data[quote]['tags']))
    return(tags)
#print(scrape_tags(data=scrape()))
def tags_input(data):
    print("You may choose your tag(s) from here\n",scrape_tags(data))
    tags=(input("Enter the tag(s) you want your quotes to have (Tags must be space-seperated): \n>> "))
    tags=tags.split()
    return tags
def number_quotes():
    number=int(input("Enter number of quotes to ouput : \n>> "))
    return number
def tags_quotes(tags, data):
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
    
    print(f"Sorry we could only find {count} quotes containing similar tags to which you entered . Here are the results\n")
    return quotes_dict

#print(json.dumps(tags_quotes(tags_input(data),data),indent=4,ensure_ascii=False))
"""---------------------------------------------------------------------------------------------------------------------------"""
#! 3.   implement the analyze function ; this function should be able to draw a chart using all the tags as X axis and map their number of instances in the Y axis 
#! 3.1. THIS IS OPTIONAL , add an input functionality to highlight a specific tag in the graph
def count_tag_instances(data):
    tag_inst_dict = {key: None for key in scrape_tags(data)}
    for quote_data in data.values():
        tags = quote_data['tags']
        for tag in tags:
            if tag in tag_inst_dict:
                if tag_inst_dict[tag] is None:
                    tag_inst_dict[tag] = 1
                else:
                    tag_inst_dict[tag] += 1
    return tag_inst_dict
def graph_tag_instance(data):
    tag_instances = count_tag_instances(data)
    sorted_tags = sorted(tag_instances.items(), key=lambda x: x[1], reverse=True)
    top_tags = [tag for tag, _ in sorted_tags[:10]]
    top_instances = [tag_instances[tag] for tag in top_tags]
    fig, ax = plt.subplots(figsize=(12, 8))
    bar_width = 0.4
    bar_spacing = 20
    max_instance = max(top_instances)
    colors = ['blue' if instance == max_instance else 'red' for instance in top_instances]
    ax.bar(range(len(top_tags)), top_instances, width=bar_width, color=colors)
    ax.set_xticks(range(len(top_tags)))
    ax.set_xticklabels(top_tags, ha='center')
    ax.set_xlabel('Top 10 Tags')
    ax.set_ylabel('Instances')
    ax.set_title('Number of Instances per Tag')
    plt.subplots_adjust(bottom=0.326, top=0.914, right=0.995, left=0.036)
    plt.show()
def scrape_authors(data):
    author_number_quotes = {}
    for quote_id, quote_info in data.items():
        author = quote_info['author']
        if author not in author_number_quotes:
            author_number_quotes[author] = {'Nb_quotes': 1}
        else:
            author_number_quotes[author]['Nb_quotes'] += 1
    return author_number_quotes
#print(json.dumps(scrape_authors(data), indent=4, ensure_ascii=False))
def graph_author_quote(data):
    author_quotes_dict = scrape_authors(data)
    sorted_authors = sorted(author_quotes_dict.items(), key=lambda x: x[1]['Nb_quotes'], reverse=True)

    top_authors = [author for author, _ in sorted_authors[:10]]
    top_quotes = [author_quotes_dict[author]['Nb_quotes'] for author in top_authors]
    fig, ax = plt.subplots(figsize=(17, 8))
    bar_width = 0.4
    bar_spacing = 20
    max_quotes = max(top_quotes)
    colors = ['blue' if quotes == max_quotes else 'red' for quotes in top_quotes]
    ax.bar(range(len(top_authors)), top_quotes, width=bar_width, color=colors)
    ax.set_xticks(range(len(top_authors)))
    ax.set_xticklabels(top_authors, ha='center')
    number_authors=len(top_authors)
    ax.set_xlabel("Authors ")
    ax.set_ylabel('Number of Quotes')
    ax.set_title(f'Top {number_authors} Authors')
    plt.subplots_adjust(bottom=0.057, top=0.914, right=0.995, left=0.048)
    plt.show()
graph_author_quote(data)








