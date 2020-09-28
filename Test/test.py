import streamlit as st 
from bs4 import BeautifulSoup
from urllib.request import urlopen
import spacy
from spacy import displacy



nlp = spacy.load('en_core_web_sm')
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""


def analyze_text(text):
	return nlp(text)



def write():
    st.title("Entity Checker")
    st.subheader("Named Entity Recognition with Spacy")
    raw_text = st.text_area("Enter Text Here")
    if st.button("Analyze"):
        docx = analyze_text(raw_text)
        html = displacy.render(docx,style="ent")
        html = html.replace("\n\n","\n")
        st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)
     


'''
def write():
    st.title("Entity Checker")
    st.subheader("Named Entity Recog with Spacy")
	raw_text = st.text_area("Enter Text Here")   
	if st.button("Analyze"):
		docx = analyze_text(raw_text)
		html = displacy.render(docx,style="ent")
		html = html.replace("\n\n","\n")
		st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)
'''