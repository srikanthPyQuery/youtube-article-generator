import streamlit as st
from summarizer import process_youtube
from pdf_generator import create_pdf

st.title("YouTube → Article Generator")

url = st.text_input("Enter YouTube URL")

if st.button("Generate"):
    if not url:
        st.error("Enter a URL")
    else:
        try:
            article = process_youtube(url)

            st.subheader("Article")
            st.write(article)

            with open("article.txt", "w", encoding="utf-8") as f:
                f.write(article)

            create_pdf(article)

            with open("output.pdf", "rb") as f:
                st.download_button("Download PDF", f, file_name="article.pdf")

        except Exception as e:
            st.error(str(e))