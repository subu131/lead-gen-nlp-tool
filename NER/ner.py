import streamlit as st 
from bs4 import BeautifulSoup
from urllib.request import urlopen
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

# Fetch Text From Url

def get_text(raw_url):
	page = urlopen(raw_url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text


#@st.cache(allow_output_mutation=True)
def analyze_text(text):
	return nlp(text)



def main():
	"""Summaryzer Streamlit App"""

	st.title("Entity Checker")

	activities = ["NER Checker","NER For URL"]
	choice = st.sidebar.selectbox("Select Activity",activities)

	
	if choice == 'NER Checker':
		st.subheader("Named Entity Recog with Spacy")
		raw_text = st.text_area("Enter Text Here","Type Here")
		if st.button("Analyze"):
			docx = analyze_text(raw_text)
			html = displacy.render(docx,style="ent")
			html = html.replace("\n\n","\n")
			st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)


	if choice == 'NER For URL':
		st.subheader("Analysis on Text From URL")
		raw_url = st.text_input("Enter URL Here","Type here")
		text_preview_length = st.slider("Length to Preview",50,100)
		if st.button("Analyze"):
			if raw_url != "Type here":
				result = get_text(raw_url)
				len_of_full_text = len(result)
				len_of_short_text = round(len(result)/text_preview_length)
				st.success("Length of Full Text::{}".format(len_of_full_text))
				st.success("Length of Short Text::{}".format(len_of_short_text))
				st.info(result[:len_of_short_text])
				summarized_docx = sumy_summarizer(result)
				docx = analyze_text(summarized_docx)
				html = displacy.render(docx,style="ent")
				html = html.replace("\n\n","\n")
				st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)
				
		


if __name__ == '__main__':
	main()
