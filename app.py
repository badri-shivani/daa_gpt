import streamlit as st
import requests

@st.cache_data
def load_notes():
    url = "https://raw.githubusercontent.com/badri-shivani/daa_gpt/main/notes.txt"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

notes_data = load_notes()

st.title("🤖 DevOps Tutor Chatbot")
st.subheader("Ask me anything about DevOps based on uploaded syllabus notes!")

user_input = st.text_area("💬 Ask your question here:", height=100)

if st.button("Get Answer"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        matching_lines = [
            line for line in notes_data.split("\n")
            if user_input.lower() in line.lower()
        ]
        if matching_lines:
            st.success("Answer from notes:")
            st.write("\n".join(matching_lines))
        else:
            st.info("No direct match found in notes. Try rephrasing.")
