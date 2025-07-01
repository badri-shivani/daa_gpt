import streamlit as st
from openai import OpenAI
import os

# Load your API key from Streamlit Secrets
api_key = st.secrets["k-xxxxxxWIcA"]

client = OpenAI(api_key=api_key)

st.title("🤖 DevOps + General GPT Assistant")
st.subheader("Ask anything — directly powered by GPT!")

question = st.text_area("💬 Ask your question here:")

if st.button("Get Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("GPT is thinking..."):
            response = client.chat.completions.create(
                model="gpt-4o",   # Or use gpt-4-turbo, etc.
                messages=[
                    {"role": "system", "content": "You are an expert DevOps tutor, answer clearly and step-by-step."},
                    {"role": "user", "content": question}
                ]
            )
            answer = response.choices[0].message.content
            st.success("Answer:")
            st.write(answer)
