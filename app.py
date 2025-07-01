import streamlit as st

# Load your notes file
@st.cache_data
def load_notes():
    with open("Notes.txt", "r", encoding="utf-8") as f:
        return f.read()

notes_data = load_notes()

# App title and subtitle
st.title("🤖 DevOps Tutor Chatbot")
st.subheader("Ask me anything about DevOps based on the uploaded syllabus notes!")

# File uploader (optional future feature)
uploaded_file = st.file_uploader("📂 Upload syllabus (future feature placeholder)", type=["pdf", "pptx"])
if uploaded_file:
    st.info("Uploaded files are not yet connected, but will be in a future release.")

# Input box for questions
user_input = st.text_area("💬 Ask your question here:", height=100)

# Simple search-based answer generation
if st.button("Get Answer"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        # naive keyword match
        matching_lines = [
            line for line in notes_data.split("\n")
            if user_input.lower() in line.lower()
        ]

        if matching_lines:
            st.success("Answer from notes:")
            st.write("\n".join(matching_lines))
        else:
            st.info("No direct match found in notes. Please try rephrasing your question.")
