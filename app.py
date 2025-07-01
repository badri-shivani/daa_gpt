import streamlit as st
from transformers import pipeline

# Load the GPT-Neo model
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

generator = load_model()

st.title("🤖 Free AI Tutor with Hugging Face GPT-Neo")

user_input = st.text_area("💬 Ask your question here:", height=100)

if st.button("Get Answer"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            output = generator(
                user_input,
                max_length=200,
                do_sample=True,
                temperature=0.7,
                top_p=0.95,
                num_return_sequences=1
            )
            answer = output[0]["generated_text"]
            st.success("Answer:")
            st.write(answer)
