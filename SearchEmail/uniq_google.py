from scraper_api import ScraperAPIClient
from bs4 import BeautifulSoup
import streamlit.components.v1 as components
import streamlit as st
import requests
import re
import base64
import SearchEmail.uniq_website

PAGES = {
    "Email from Domain" : SearchEmail.uniq_website,
    
}



client = ScraperAPIClient('a9b8ffec68ce01306b509ca71475fad9')

#Google Email Scraper
def scrape(name,search_String):   
    
    err = "Error"

    try:
        search = name + " " + "@" + search_String.lower() + "&num=100"
        url = 'https://www.google.com/search?q=' + search
        
        url2 = 'https://www.google.com/search?q=@' + search_String.lower() + "&num=100"

        result = client.get(url=url2, country_code = "in").text
        soup = BeautifulSoup(result,'html.parser')

        headlines = soup.find_all('div',class_='s')
        
        email_list = []
        none = "None"

        for h in headlines:    
            email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", h.text)
            if email:
                for i in email:
                    a = "@"+search_String
                    if a in i:
                        email_list.append(i)            
        #print(email_list)
        if email_list:
            return set(email_list)
        else:
            #url2 = 'https://www.google.com/search?q=@' + search_String + "&num=100"

            result = client.get(url=url, country_code = "in").text
            soup = BeautifulSoup(result,'html.parser')

            headlines = soup.find_all('div',class_='s')
            for h in headlines:    
                email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", h.text)
                if email:
                    for i in email:
                        if search_String.lower() in i:
                            email_list.append(i)
            if email_list:
                return set(email_list)
            else:
                return none     
    except Exception as e:
        return e

def write():

    selection = st.sidebar.radio("Go to", ["Email from Google Search","Email from Domain"])

    if selection == "Email from Google Search":

        components.html(
            '''        
            <h1><font face="Digital, Arial, Helvetica, sans-serif">Emails from Google Search  </font> <img src="https://i.pinimg.com/originals/8c/03/0b/8c030bd6bd7ee87ad41485e3c7598dd4.png" alt="HTML5 Icon" width="30";height="30"><h1/>
            ''',
            height=60,    
        )

        name = st.text_input("Full Name"," ")
        website = st.text_input("Website","Url")

        if st.button("Search"):
            try:
                emails = scrape(name,website)
                if emails:
                    st.write(" ")
                    st.markdown("###   Found Emails")
                    st.success(", ".join(emails))
                else:
                    st.warning("Not Found")
            except Exception as e:
                st.error(e)
    if selection == "Email from Domain":
        page = PAGES["Email from Domain"]

        with st.spinner(f'Loading {selection} ...'):
            page.write()
        




