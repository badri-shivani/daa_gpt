import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline

# load summarizer
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="model="t5-small")

summarizer = load_summarizer()

# read pdf lines
@st.cache_data
def load_syllabus_lines():
    lines = []
    with fitz.open("DevOps-Notes.pdf") as doc:
        for page in doc:
            page_text = page.get_text()
            lines.extend(page_text.split("\n"))
    return [line.strip() for line in lines if line.strip()]

syllabus_lines = load_syllabus_lines()

st.title("🤖 DevOps Tutor Chatbot")
st.subheader("Ask me anything from the syllabus!")

user_input = st.text_area("💬 Ask your question here:", height=100)

if st.button("Get Answer"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        # find relevant lines
        relevant = [
            line for line in syllabus_lines
            if user_input.lower() in line.lower()
        ]
        if relevant:
            relevant_text = " ".join(relevant)
            # avoid huge input
            if len(relevant_text) > 1500:
                relevant_text = relevant_text[:1500]
            with st.spinner("Generating simplified notes..."):
                summary = summarizer(
                    relevant_text,
                    max_length=150,
                    min_length=30,
                    do_sample=False
                )[0]['summary_text']
                st.success("Simplified notes:")
                st.write(summary)
        else:
            st.info("No direct match found. Please try rephrasing your question.")
