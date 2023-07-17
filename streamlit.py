import streamlit as st
import time
from streamlit_functions import *
from PIL import Image
st.set_page_config(layout="wide",page_icon="💭")

     
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




reply_forum=st.form(key="reply")

reply = reply_forum.radio("Do you want all the website content ? ",
                 options=("No", "Yes"))
#! the radio widget in streamlit is like a multichoice question
if reply == "No":
    pages_number = reply_forum.number_input(
        "How many pages to scrape ? ", min_value=1, max_value=9,value=1)
else:
    pages_number = 10
scrape_button = reply_forum.form_submit_button(f"Scrape")
@st.cache_data()
def Scrape_data(pages_number):
     data=st_scrape(pages_number)
     return data
data_dict={}
if scrape_button:
    data_dict = Scrape_data(pages_number)




#!Scrapping and calculating run time : start 
start = time.time()
end = time.time()-start
#!Scrapping and calculating run time : finish  

#if scrape_button == True:
    #reply_forum.write("Scraping starting ...\n")
    #time.sleep(round(end,2))
    #reply_forum.write("\nScrapping ended\n")
    #reply_forum.write(f"Execution time : {round(end,2)} seconds")
    #st.markdown("---")

author_info_forum=st.form(key="author info")

author_name = author_info_forum.selectbox("Select an author to Display their information",
                           options=st_unique_authors(data_dict))
author_link=author_bio_link(author_name,data_dict)
#author_link_button=st.button(f"Display {author_name} Bio link")
author_quotes_button = author_info_forum.form_submit_button(f"Display information")
quotes_column,author_link_column=author_info_forum.columns(2)





if author_quotes_button:
        quotes = st_author_quotes(author_name, data_dict)
        quotes_column.header(f"{author_name} Quotes")
        for quote in quotes:
            quotes_column.write(quote)
        #scrape_image(author_name)
        edited_author_name=author_name.replace(" ",'_')
        #image=Image.open(f'Author pictures/{edited_author_name}.jpg ')
        author_link_column.header(f"{author_name} Image")
        st_scrape_image(author_name,author_link_column)
        #author_link_column.image(image,use_column_width="auto")
        author_link_column.markdown("---")
        author_link_column.header(f"{author_name} Bio link")
        author_link_column.write(author_link)





tags_form=st.form(key="tags")

tags = tags_form.multiselect("Select the tag(s) to display quotes with similar tags",
                      options=st_filter_tags(data_dict))
number = tags_form.number_input(
    "Select the number of quotes to display", max_value=10, min_value=1, value=1)
display_quotes_button = tags_form.form_submit_button("Display quotes")
if display_quotes_button:
    quotes = st_tags_quotes(tags, data_dict, number=number)
    for quote in quotes:
        tags_form.write(quote['quote'] + ' ' + quote['author'])


graph_form=st.form(key="graph")
graph_form.header("graphs")
tag_instances_column,author_quotes_column=graph_form.columns(2)

show_graphs=graph_form.form_submit_button("Display graphs")

if show_graphs:
     with tag_instances_column:
        fig1=st_graph_tag_instance(data_dict)
        tag_instances_column.plotly_chart(fig1)
          
     with author_quotes_column:
        fig2 = st_graph_author_quote(data_dict)
        author_quotes_column.plotly_chart(fig2)