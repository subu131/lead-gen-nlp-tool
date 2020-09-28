from scraper_api import ScraperAPIClient
from bs4 import BeautifulSoup
import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
import io
import requests
import re
import base64
import BulkEmail.scrape_hunter

PAGES = {
    "Email from Hunter" : BulkEmail.scrape_hunter,
    
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
                    if search_String in i:
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
    except:
        return err





#generate download link
def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>( right click to save the file)'
    return href

def write():

    #set slider at start    
    #st.beta_set_page_config(
	#initial_sidebar_state="collapsed",  # Can be "auto", "expanded", "collapsed"
	#)


    #activities = ["Emails from Google","Scrape Website"]
    #choice = st.sidebar.selectbox("Select Activities",activities)

    try:

        selection = st.sidebar.radio("Go to", ["Email from Google Search","Email from Hunter"])

        if selection == "Email from Google Search":

            components.html(
            '''        
            <h1> <font face="Digital, Arial, Helvetica, sans-serif">Scrape Emails  </font>   <img src="https://image.flaticon.com/icons/png/512/281/281769.png" width="20";height="20"> <h1>
            ''',
            height=65,    
            )

            
            
            st.subheader("Bulk Email from Google Search")
            st.info("**Input**: text file with firstName & website    \n"
                    "**Output**: csv file with firstName, website & emails    \n")
            
            st.write(" ")
            uploaded_file = st.file_uploader('Upload your csv file',type=['csv','txt'],encoding =None)

            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                if st.checkbox("Preview File"):
                    st.dataframe(df.head())
                
                if st.button("Scrape"):
                    li = []
                    for i in range(len(df)):
                        fullName = df.iloc[i,0].strip()
                        website = df.iloc[i,1].strip()
                        email = scrape(fullName,website)
                        st.text(i)
                        li.append(email)
                    df["Email"] = li

                    st.dataframe(df.head())
                    st.markdown(get_table_download_link(df), unsafe_allow_html=True)

        if selection == "Email from Hunter":
            page = PAGES["Email from Hunter"]

            with st.spinner(f'Loading {selection} ...'):
                page.write()
        
        
        
                    
    except Exception as e:
        st.error(e)    
         
    
#if __name__ == '__main__':
#	main() 

   