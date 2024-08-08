from deep_translator import GoogleTranslator
import streamlit as st
st.set_page_config(page_title="NLP Web App",page_icon="🧊",layout="centered",initial_sidebar_state="auto")

# NLP Pkgs
from textblob import TextBlob
import spacy
import neattext as nt 

# Viz Pkgs
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from wordcloud import WordCloud

#import spacy

# Import the Google Translator library
from googletrans import Translator 


from collections import Counter
import re 

def summarize_text(text,num_sentences=3):
    # Remove special characters and convert text to lowercase
    clean_text = re.sub('[^A-Za-z0-9]+', ' ', text).lower()
    # Split text into words
    words = clean_text.split()

    # Calculate frequency of each word
    word_freq = Counter(words)

    # Sort the words based on their frequency in descending order
    sorted_words = sorted(word_freq, key=word_freq.get, reverse=True)
    # Extract the top 'num_sentences' sentences based on frequency of words
    top_words = sorted_words[:num_sentences]

    # Create the summary by joining the top words
    summary = ' '.join(top_words)
    return

@st.cache_data
# Lemma and Tokens Function
def text_analyzer(text):
    # import English library
    nlp = spacy.load('en_core_web_sm')
    # create an nlp object
    doc = nlp(text)
    #extract tokens and lemmas
    allData =[('"Token":{},\n"Lemma":{}'.format(token.text,token.lemma_)) for token in doc]
    return allData


def main():
    """ NLP App with Streamlit """

    title_template = """
    <div style="background-color:blue;padding:10px;border-radius:10px">
    <h1 style="color:cyan;text-align:center;">NLP Web App</h1>
    </div>
    """
    st.markdown(title_template,unsafe_allow_html=True)

    subheader_template = """
    <div style="background-color:cyan;padding:10px;border-radius:10px">
    <h3 style="color:blue;text-align:center;">Natural Language Processing</h3>
    </div>
    """
    st.markdown(subheader_template,unsafe_allow_html=True)

    st.sidebar.image("nlp.jpg",use_column_width=True)


    st.title("NLP Web App")
    activity=["Text Analysis","Translation","Sentiment Analysis","About"]
    choice = st.sidebar.selectbox("Menu",activity)

    if choice == 'Text Analysis':
        st.subheader("Text Analysis")
        st.write("")

        raw_text = st.text_area("Write Something","Enter a text in English...",height=300)    

        if st.button("Analyze"):
            if len(raw_text) == 0:
                st.warning("Please enter a text")
            else:
                blob = TextBlob(raw_text)
                st.info("Bsic Functions")
                st.write("OK")

                col1, col2 = st.columns(2)
                
                with col1:
                    with st.expander("Bsic Info"):
                        st.info("Text Stats")
                        word_desc = nt.TextFrame(raw_text).word_stats()
                        result_desc = {"Length of Text":word_desc['Length of Text'],
                                       "Num of Vowels":word_desc['Num of Vowels'],
                                       "Num of Consonants":word_desc['Num of Consonants'],
                                       "Num of Stopwords":word_desc['Num of Stopwords']}
                        st.write(result_desc)              
                    with st.expander("Stopwords"):
                        st.success("Stop Words List")
                        stop_w = nt.TextExtractor(raw_text).extract_stopwords()
                        st.error(stop_w)                 

                with col2:
                    with st.expander("Processed Text"):
                        st.success("Stopwords Excluded Text")
                        processed_text = str(nt.TextFrame(raw_text).remove_stopwords())
                        st.write(processed_text)

                    with st.expander("Plot WordCloud"):
                        st.success("Word Cloud")
                        word_cloud = WordCloud().generate(processed_text) 
                        plt.imshow(word_cloud,interpolation='bilinear')
                        plt.axis("off")
                        st.pyplot(fig=plt)    
                st.write("")
                st.write("")
                st.info("Advanced Features")

                col3,col4 = st.columns(2)
                with col3:
                    with st.expander("Tokens & Lemma"):
                        st.write("Tokens & Lemma")
                        processed_text_mid = str(nt.TextFrame(raw_text).remove_stopwords())
                        processed_text_mid = str(nt.TextFrame(processed_text_mid).remove_puncts())
                        processed_text_fin = str(nt.TextFrame(processed_text_mid).remove_special_characters())
                        tandl = text_analyzer(processed_text_fin)
                        st.json(tandl)
                with col4:
                    with st.expander("Summarize"):
                        st.success("Summarize")  
                        summary = summarize_text(raw_text)     
    if choice == 'Translation':
        st.subheader("Translation")
        st.write("")
        raw_text = st.text_area("Original Text", "Write something to be translated...",height=300)
        if len(raw_text) < 3:
            st.warning("Please provide a text with at least 3 characters.")
        else:
            target_lang = st.selectbox("Select Language",["German","Spanish","French","Italian"])
            if target_lang == "German":
                target_lang = "de"
            elif target_lang == "Spanish":
                target_lang = "es"
            elif target_lang == "French":
                target_lang = "fr"
            else:
                target_lang = "it"
        if st.button("Translate"):
            translator = GoogleTranslator(source='auto', target=target_lang)
            translated_text = translator.translate(raw_text)
            st.write(translated_text)            
    if choice == 'Sentiment Analysis':
        st.subheader("Sentiment Analysis")
        st.write("")    
        raw_text = st.text_area("Text to analyse","Enter a text in English...",height=300)
        if st.button("Analyze"):
            if len(raw_text) == 0:
                st.warning("Please enter a text")
            else:
                blob = TextBlob(raw_text)
                st.info("sentiment Analysis")
                st.write(blob.sentiment)
                st.write("")
    if choice == 'About':
        st.subheader("About")
        st.write("")

        st.markdown("""
                    ### NLP Web App made with Streamlit
                    
                    for info:
                    - [streamlit](https://streamlit.io)
                    """)
        
if __name__ == '__main__':
    main()
    


        