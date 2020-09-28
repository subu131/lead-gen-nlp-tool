import requests
import pandas as pd
import streamlit as st
import base64
import streamlit.components.v1 as components


def title_awesome(body: str):
    """Uses st.write to write the title as f'Awesome Streamlit {body}'
    - plus the awesome badge
    - plus a link to the awesome-streamlit GitHub page
    Arguments:
        body {str} -- [description]
    """
    st.write(
        f"# Awesome Streamlit {body} "
        "[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/"
        "d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)]"
        "(https://github.com/MarcSkovMadsen/awesome-streamlit)"
    )


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>( right click to save the file)'
    return href



def email_from_hunter(first_name,last_name,domain,api):

    try:
        url = f"https://api.hunter.io/v2/email-finder?domain={domain}&first_name={first_name}&last_name={last_name}&api_key={api}"
        result = "Not Found"
        res = requests.get(url)
        data = res.json()
        email = data['data']['email']    
        if email:
            return email
        else:
            return result
    except Exception as e:
        return e


def write():

    
    components.html(
        '''        
        <h1> <font face="Digital, Arial, Helvetica, sans-serif">Emails From Hunter </font>   <img src="https://hunter.io/images/icon_512x512.png" width="40";height="40"> <h1>
        ''',
        height=80,    
    )

    st.info(
        "Handles [**Hunter.io**'s](https://hunter.io/) email API.   \n"
        "**Input** : csv file with firstname,lastname & website    \n"
        "**Output** : csv with email. "
        
    )

    st.title(" ")
    

    api = st.text_input("Api key")

    uploaded_file = st.file_uploader('Upload your csv file',type=['csv','txt'],encoding =None)

    if st.button("Scrape"):
        if api:
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                #if st.checkbox("Preview File"):
                    #st.dataframe(df.head())
                                
                li = []
                for i in range(len(df)):
                    first_name = df.iloc[i,0].strip()
                    last_name = df.iloc[i,1].strip()
                    domain = df.iloc[i,2].strip()
                    email = email_from_hunter(first_name,last_name,domain,api)
                    li.append(email)
                    st.text(i)
                df['email'] = li

                st.dataframe(df.head())
                st.markdown(get_table_download_link(df), unsafe_allow_html=True) 
            else:
                st.error("upload file")                        
        else:
            st.error("Provide API")



#main()








