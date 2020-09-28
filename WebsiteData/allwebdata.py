from scraper_api import ScraperAPIClient
import streamlit as st
import requests
import re
from bs4 import BeautifulSoup 
import streamlit.components.v1 as components
import spacy
import WebsiteData.specificdata


PAGES = {
    "Specific Data" : WebsiteData.specificdata,
    
}


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
    social_link.linkedin = []

    for link in soup.find_all('a',href=True):
        hrefs = link['href']
        if "facebook.com" in hrefs:
            social_link.fb.append(hrefs)   
        if "youtube.com" in hrefs:
            social_link.yt.append(hrefs) 
        if "instagram.com" in hrefs:
            social_link.insta.append(hrefs)
        if "linkedin.com" in hrefs:
            social_link.linkedin.append(hrefs)
                




    

   

#scrape through request library
def write():
    
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent" : USER_AGENT}


    selection = st.sidebar.radio("Go to", ["Data from Website","Specific Data"])

    if selection == "Data from Website":        

        
        components.html(
            '''        
            <h1><font face="Digital, Arial, Helvetica, sans-serif">Website Data </font> <img src="https://www.pngkit.com/png/detail/205-2055556_free-icons-png-web-icon-round-png.png" alt="HTML5 Icon" width="30";height="30"><h1/>
            ''',
            height=60,    
        )
    
        st.info("Scrapes data from website.")
        st.text("")
        st.write("")
        
        url = st.text_input("Enter The URL","Url..")



        if st.button("Go"):
            try:
                res = requests.get(url,headers=headers)
                final_url = res.url
                soup = BeautifulSoup(res.text,'html.parser')

                li = ["jhgf","hgkj","ggg"]

                title = soup.find('title')
                title_text = title.string


                st.subheader("Domain :")
                st.text(final_url)    

                st.subheader("Title :")
                st.text(title_text)

                st.subheader("Email : ")
                a = email(soup,final_url)
                if a != "None":
                    st.text(", ".join(a))
                else:
                    st.text("Not Found")    
                
                
                st.subheader("Facebook : ")
                social_link(soup)
                if social_link.fb:
                    st.text("   " + social_link.fb[0])
                else:
                    st.text("Not Found")


                st.subheader("Linkedin : ")
                if social_link.linkedin:
                    st.text(social_link.linkedin[0])
                else:
                    st.text("Not Found")


                st.subheader("Instagram : ")
                if social_link.insta:
                    st.text(social_link.insta[0])
                else:
                    st.text("Not Found")


                st.subheader("Youtube : ")
                if social_link.yt:
                    st.text(social_link.yt[0])
                else:
                    st.text("Not Found")
            except Exception as e:
                st.error(e)
    if selection == "Specific Data":
        page = PAGES["Specific Data"]

        

        with st.spinner(f'Loading {selection} ...'):
            page.write()



#main()


