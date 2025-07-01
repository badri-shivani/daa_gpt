import streamlit as st
import fitz  # PyMuPDF

@st.cache_data
def load_syllabus_lines():
    lines = []
    with fitz.open("DevOps-Notes.pdf") as doc:
        for page in doc:
            page_text = page.get_text()
            lines.extend(page_text.split("\n"))
    # remove empty lines and strip whitespace
    clean_lines = [line.strip() for line in lines if line.strip()]
    return clean_lines

syllabus_lines = load_syllabus_lines()

st.title("🤖 DevOps Tutor Chatbot")
st.subheader("Ask me anything from the syllabus!")

user_input = st.text_area("💬 Ask your question here:", height=100)

if st.button("Get Answer"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        # exact matching lines
        matching_lines = [
            line for line in syllabus_lines
            if user_input.lower() in line.lower()
        ]
        if matching_lines:
            st.success("Answer from syllabus:")
            for line in matching_lines:
                st.write(f"👉 {line}")
        else:
            st.info("No direct match found. Try rephrasing your question.")
