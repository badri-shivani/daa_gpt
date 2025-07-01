import streamlit as st
import fitz  # PyMuPDF

# Read the syllabus.pdf directly from the repo
@st.cache_data
def load_syllabus_text():
    text = ""
    with fitz.open("DevOps-Notes.pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

syllabus_text = load_syllabus_text()

st.title("🤖 DevOps Tutor Chatbot")
st.subheader("Ask me anything from the syllabus!")

user_input = st.text_area("💬 Ask your question here:", height=100)

if st.button("Get Answer"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        matching_lines = [
            line for line in syllabus_text.split("\n")
            if user_input.lower() in line.lower()
        ]
        if matching_lines:
            st.success("Answer from syllabus:")
            st.write("\n".join(matching_lines))
        else:
            st.info("No direct match found. Try rephrasing your question.")
