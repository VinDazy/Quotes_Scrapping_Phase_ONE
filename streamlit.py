import streamlit as st
import time
from streamlit_functions import *
from PIL import Image



st.title("   Web scrapping analysis app ")
st.markdown("""
<style>
.css-eh5xgm.e1ewe7hr3    
{
            visibility : hidden;
}
.css-cio0dv.e1g8pov61
            {
            visibility : hidden;
            }
</style>
""", unsafe_allow_html=True)
st.markdown("---")

reply = st.radio("Do you want all the website content ? ",
                 options=("No", "Yes"))
#! the radio widget in streamlit is like a multichoice question
if reply == "No":
    pages_number = st.number_input(
        "How many pages to scrape ? ", min_value=1, max_value=9, value=1)
else:
    pages_number = 10

scrape_button = st.button(f"Scrape {pages_number} pages")
#!Scrapping and calculating run time : start 
start = time.time()
data_dict = st_scrape(pages_number)
end = time.time()-start
#!Scrapping and calculating run time : finish  




author_name = st.selectbox("Select an author to Display their information",
                           options=st_unique_authors(data_dict))
author_link=author_bio_link(author_name,data_dict)
#author_link_button=st.button(f"Display {author_name} Bio link")
author_quotes_button = st.button(f"Display {author_name} information")
quotes_column,author_link_column=st.columns(2)

st.markdown("---")



if scrape_button == True:
    st.write("Scraping starting ...\n")
    time.sleep(round(end,2))
    st.write("\nScrapping ended\n")
    st.write(f"Execution time : {round(end,2)} seconds")
    #st.markdown("---")





if author_quotes_button:
        quotes = st_author_quotes(author_name, data_dict)
        for quote in quotes:
            quotes_column.write(quote)
        image=Image.open('Author pictures/Einstein.jpg ')
        author_link_column.image(image,use_column_width="auto")
        author_link_column.write(author_link)





tags = st.multiselect("Select the tag(s) to display quotes with similar tags",
                      options=st_filter_tags(data_dict))
number = st.number_input(
    "Select the number of quotes to display", max_value=10, min_value=1, value=1)
display_quotes_button = st.button("Display quotes")
if display_quotes_button:
    quotes = st_tags_quotes(tags, data_dict, number=number)
    for quote in quotes:
        st.write(quote['quote'] + ' ' + quote['author'])
print(pages_number)