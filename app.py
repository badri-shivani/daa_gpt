import streamlit as st
import fitz
from transformers import pipeline

@st.cache_resource
def load_qa():
    return pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

qa = load_qa()

@st.cache_data
def load_pdf_lines():
    lines = []
    with fitz.open("DevOps-Notes.pdf") as doc:
        for page in doc:
            lines.extend(page.get_text().split("\n"))
    return [l.strip() for l in lines if l.strip()]

pdf_lines = load_pdf_lines()

st.title("🤖 DevOps Tutor Chatbot")
st.subheader("Ask me anything from the syllabus!")

question = st.text_area("💬 Ask your question here:", height=100)

if st.button("Get Answer"):
    if not question.strip():
        st.warning("Please ask something.")
    else:
        relevant = [line for line in pdf_lines if question.lower() in line.lower()]
        if relevant:
            context = " ".join(relevant)
            if len(context) > 1500:
                context = context[:1500]
            with st.spinner("Thinking..."):
                result = qa({
                    "question": question,
                    "context": context
                })
                answer = result["answer"]
                st.success("Answer (detailed):")
                for s in answer.split("."):
                    if s.strip():
                        st.write("👉", s.strip())
        else:
            st.info("No match found. Please try rephrasing your question.")
