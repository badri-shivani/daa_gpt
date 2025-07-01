import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="🤖 DevOps Tutor", page_icon="🤖", layout="wide")

st.title("🤖 DevOps Tutor Chatbot")
st.subheader("Ask anything from your DevOps syllabus and get clear, concept-based answers!")

# 1️⃣ chunk PDF into chunks
@st.cache_data
def chunk_pdf(file_path, chunk_size=200):
    chunks = []
    with fitz.open(file_path) as doc:
        for page in doc:
            text = page.get_text()
            words = text.split()
            for i in range(0, len(words), chunk_size):
                chunk = " ".join(words[i:i+chunk_size])
                chunks.append(chunk)
    return chunks

chunks = chunk_pdf("DevOps-Notes.pdf")

# 2️⃣ load embedding model
@st.cache_resource
def load_embedder():
    return SentenceTransformer('all-MiniLM-L6-v2')

embedder = load_embedder()

# 3️⃣ embed all chunks
@st.cache_resource
def embed_chunks(chunks):
    return embedder.encode(chunks)

chunk_embeddings = embed_chunks(chunks)

# 4️⃣ load QA pipeline
@st.cache_resource
def load_qa():
    return pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

qa = load_qa()

# 5️⃣ user input
user_question = st.text_area("💬 Ask your DevOps question here:", height=100)

if st.button("Get Answer"):
    if not user_question.strip():
        st.warning("Please enter a question.")
    else:
        # embed the question
        with st.spinner("Finding best matching section..."):
            question_embedding = embedder.encode([user_question])
            sims = cosine_similarity(question_embedding, chunk_embeddings)
            best_idx = sims.argmax()
            best_chunk = chunks[best_idx]
        
        # pass best chunk to QA
        with st.spinner("Generating answer..."):
            result = qa({
                "question": user_question,
                "context": best_chunk
            })
            answer = result["answer"]

            # break answer into steps if long
            st.success("Answer:")
            for step in answer.split("."):
                if step.strip():
                    st.write("👉", step.strip())

        st.info(f"🔎 Answer based on most relevant chunk of your notes.")
