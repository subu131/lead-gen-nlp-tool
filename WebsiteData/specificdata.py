from scraper_api import ScraperAPIClient
import awesome_streamlit as ast
import streamlit as st
import requests
import re
from bs4 import BeautifulSoup 
import streamlit.components.v1 as components

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
headers = {"user-agent" : USER_AGENT}



def clean(data_to_clean):
            data = re.sub('[^a-zA-Z0-9 \. ]','',data_to_clean)
            cleaned_data = " ".join(data.split())
            return cleaned_data

def cleanText(text):
    # kill all script and style elements
    #for script in soup(["script", "style"]):
    #    script.extract()    # rip it out

    # get text
    #text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


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
    

def social_link(soup):
    social_link.fb = []
    social_link.yt = []
    social_link.insta = []

    for link in soup.find_all('a',href=True):
        hrefs = link['href']
        if "facebook.com" in hrefs:
            social_link.fb.append(hrefs)   
        if "youtube.com" in hrefs:
            social_link.yt.append(hrefs) 
        if "instagram.com" in hrefs:
            social_link.insta.append(hrefs)



def li_of_alllinks(soup):
    li_of_alllinks = []
    for link in soup.find_all('a', href=True):
        hrefs = link['href']
        li_of_alllinks.append(hrefs)    
        #if final_url in hrefs:
            #li_of_alllinks.append(hrefs)
    return li_of_alllinks

def parah(soup):
    p_tags = " ".join([i.text for i in soup.find_all('p')])
    p_tags = cleanText(p_tags)
    return p_tags

def h1(soup):
    h1 = " ".join([i.text for i in soup.find_all('h1')])
    return h1

def h2(soup):
    h2 = " ".join([i.text for i in soup.find_all('h2')])
    return h2

def h3(soup):
    h3 = " ".join([i.text for i in soup.find_all('h3')])
    return h3

def h4(soup):
    h4 = " ".join([i.text for i in soup.find_all('h4')])
    return h4

def h5(soup):
    h5 = " ".join([i.text for i in soup.find_all('h5')])
    return h5

def h6(soup):
    h6 = " ".join([i.text for i in soup.find_all('h6')])
    return h6

def title(soup):
    title_ = soup.find("title")
    return title_.string



def write():

    st.title("Scrape Website tags")

    url = st.text_input("Enter The URL","Url..")


    tag_list = ["title","h1","h2","h3","h4","h5","h6","p","links","footer"]

    choice = st.selectbox("",tag_list)

    if st.button("Go"):
        try:
            res = requests.get(url,headers=headers)
            final_url = res.url
            soup = BeautifulSoup(res.text,'html.parser')

            if choice == "title":
                ti = title(soup)
                st.subheader("Title:")
                if ti:                    
                    st.write(ti)
                else:
                    st.write("none")

            if choice == "h1":
                h1_ = h1(soup)
                st.subheader("h1:")
                if h1_:                    
                    st.write(h1_)
                else:
                    st.write("none")

            if choice == "h2":
                h2_ = h2(soup)
                st.subheader("h2 :")
                if h2_:                    
                    st.write(h2_)
                else:
                    st.write("none")


            if choice == "h3":
                h3_ = h3(soup)
                st.subheader("h3:")
                if h3_:                    
                    st.write(h3_)
                else:
                    st.write("none")

            if choice == "h4":
                h4_ = h4(soup)
                st.subheader("h4:")
                if h4_:
                    st.write(h4_)
                else:
                    st.write("none")    

            if choice == "h5":
                h5_ = h5(soup)
                st.subheader("h5:")
                if h5_:
                    st.write(h5_)
                else:
                    st.write("none")

            if choice == "h6":
                h6_ = h6(soup)
                st.subheader("h6:")
                if h6_:
                    st.write(h6_)
                else:
                    st.write("none")    

            if choice == "p":
                p = parah(soup)
                st.subheader("P:")
                if p:
                    st.markdown(p)
                else:
                    st.write("none")    

            if choice == "links":
                link = li_of_alllinks(soup)
                st.subheader("Links :")
                if link:
                    for i in link:
                        st.markdown(i)
                else:
                    st.write("none")        



        except Exception as e:
            st.error(e)    










        









