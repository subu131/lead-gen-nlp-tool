import streamlit as st

import awesome_streamlit as ast
import WebsiteData.allwebdata
import SearchEmail.uniq_google
import BulkEmail.email_google
import NER.ner
import Test.test

#ast.core.services.other.set_logging_format()

PAGES = {
    "Website Data": WebsiteData.allwebdata,
    "Search Email": SearchEmail.uniq_google,
    "Bulk Email": BulkEmail.email_google,
    "NER" : Test.test
    
}


def main():
    """Main function of the App"""
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("", list(PAGES.keys()))

    

    page = PAGES[selection]

    #with st.spinner(f"Loading {selection} ..."):
    
    ast.shared.components.write_page(page)
    
    st.sidebar.title("About")
    st.sidebar.info(
        """
        This app is made to ease the process of gathering Business emails for **Lead Generation**.
        The informations scraped are from publicly avaialable data. 
        """
    )


if __name__ == "__main__":
    main()