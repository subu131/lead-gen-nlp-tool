from scraper_api import ScraperAPIClient
import streamlit as st
import requests
import re
from bs4 import BeautifulSoup 
import streamlit.components.v1 as components
import spacy


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
headers = {"user-agent" : USER_AGENT}


def get_contact_link(soup,final_url):

    li = ["/contact","/contact-us"]

    contact_link = ""

    #extract contact link     
    for link in soup.find_all('a',href=True):
        hrefs = link['href']    
        #looks for "/contact" in href and concats url
        if hrefs in li:
            contact_link = final_url[0:-1] + hrefs
            #print("Concated link")
            #print(contact_link) 
            break
        
        if li[0] in hrefs:
            contact_link = hrefs
            break
        elif li[1] in hrefs:
            contact_link = hrefs
            break
    return contact_link



def email(soup,final_url):
    text = soup.findAll(text=True)
    emails = []
    null = "None"
    email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(text))
    
    if email:    
        for i in email:
            emails.append(i)
        return emails    
    else:
        contact_link = get_contact_link(soup,final_url)
        #st.text(contact_link)
        if not contact_link:
            return null
        else:
            res_contact = requests.get(contact_link,headers=headers)
            soup_contact = BeautifulSoup(res_contact.text,'html.parser')
            text_contact = soup_contact.findAll(text=True)
            email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(text_contact))
            #st.text(email)
            if email:    
                for i in email:
                    emails.append(i)
                return emails    
            else:
                return null


def write():
    
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent" : USER_AGENT}


    #st.sidebar.radio("Go to", ["Abc","fgd"])



    
    components.html(
        '''        
        <h1><font face="Digital, Arial, Helvetica, sans-serif">Emails from Website  </font> <img src="https://www.pngkit.com/png/detail/205-2055556_free-icons-png-web-icon-round-png.png" alt="HTML5 Icon" width="30";height="30"><h1/>
        ''',
        height=60,    
    )
 
    st.text("")
    st.write("")
    
    url = st.text_input("Enter The URL","Url..")



    if st.button("Go"):
        try:
            res = requests.get(url,headers=headers)
            final_url = res.url
            soup = BeautifulSoup(res.text,'html.parser')
          
            #st.subheader("Email : ")
            a = email(soup,final_url)
            
            if a != None:
                st.markdown("Found Emails")
                st.success(", ".join(a))
            else:
                st.markdown("Found Emails")
                st.warning("None")
        except Exception as e:
            st.error(e)


