import streamlit as st
import fitz
from transformers import pipeline

# Load QA pipeline
@st.cache_resource
def load_qa():
    return pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

qa = load_qa()

# Load PDF
@st.cache_data
def load_pdf_lines():
    lines = []
    with fitz.open("DevOps-Notes.pdf") as doc:
        for page in doc:
            lines.extend(page.get_text().split("\n"))
    return [l.strip() for l in lines if l.strip()]

pdf_lines = load_pdf_lines()

st.title("🤖 DevOps Tutor with Steps")
st.subheader("Ask detailed questions from your syllabus")

user_input = st.text_area("Your question:")

if st.button("Get Answer"):
    if not user_input.strip():
        st.warning("Please ask a question.")
    else:
        relevant = [
            line for line in pdf_lines
            if user_input.lower() in line.lower()
        ]
        if relevant:
            # Combine relevant text but limit size
            relevant_text = " ".join(relevant)
            if len(relevant_text) > 1500:
                relevant_text = relevant_text[:1500]
            with st.spinner("Finding answer..."):
                result = qa({
                    "context": relevant_text,
                    "question": user_input
                })
                answer = result["answer"]
                st.success("Answer (broken down):")
                for step in answer.split("."):
                    if step.strip():
                        st.write("👉 " + step.strip())
        else:
            st.info("No match found. Try rephrasing.")
