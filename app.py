import streamlit as st
from transformers import pipeline

# load a small free open model
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

generator = load_model()

st.title("🤖 DevOps Tutor Chatbot")

user_input = st.text_area("💬 Ask your question here:", height=100)

if st.button("Get Answer"):
    if not user_input.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating..."):
            result = generator(
                user_input,
                max_length=200,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
            st.success("Answer:")
            st.write(result[0]["generated_text"])
