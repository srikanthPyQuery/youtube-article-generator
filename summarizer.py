import os
from dotenv import load_dotenv
from langchain_community.document_loaders import YoutubeLoader
from groq import Groq
import streamlit as st

load_dotenv()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])



def extract_transcript(url):
    loader = YoutubeLoader.from_youtube_url(url)
    docs = loader.load()

    if not docs:
        raise ValueError("No transcript available")

    return docs[0].page_content

def generate_article(text):
    prompt = f"""
Convert this YouTube transcript into a professional article.

Rules:
- Remove intro, ads, promotions
- Focus only on useful content
- Use headings and bullet points
- Add actionable steps
- End with summary

Content:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # stable on Groq
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def process_youtube(url):
    transcript = extract_transcript(url)

    if len(transcript) > 5000:
        chunks = [transcript[i:i + 5000] for i in range(0, len(transcript), 5000)]

        summaries = []
        for chunk in chunks:
            summaries.append(generate_article(chunk))

        # 🔥 STRONG final merge prompt
        final_prompt = f"""
You are a professional editor.

Merge the following into ONE clean article:

Rules:
- Remove repetition completely
- Maintain logical flow
- Use proper headings
- Keep it concise and structured
- One introduction, one conclusion

Content:
{summaries}
"""

        return generate_article(final_prompt)

    else:
        return generate_article(transcript)
