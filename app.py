import streamlit as st
import fitz
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from googleapiclient.discovery import build

st.set_page_config(page_title="🤖 DevOps Tutor", page_icon="🤖", layout="wide")

# 1️⃣ PDF chunking
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

# 2️⃣ embedding model
@st.cache_resource
def load_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")

embedder = load_embedder()

@st.cache_resource
def embed_chunks(chunks):
    return embedder.encode(chunks)

chunk_embeddings = embed_chunks(chunks)

# 3️⃣ QA pipeline
@st.cache_resource
def load_qa():
    return pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

qa = load_qa()

# 4️⃣ Google search fallback
api_key = "YOUR_GOOGLE_API_KEY"  # replace with your API key
cse_id = "e15a2d9c1870c4b49"

def google_search(query):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, num=3).execute()
    if 'items' in res:
        return [item['snippet'] for item in res['items']]
    else:
        return []

# 5️⃣ UI
st.title("🤖 DevOps Tutor Chatbot")
st.subheader("Ask anything from your syllabus, or I'll try to look it up online!")

question = st.text_area("💬 Ask your DevOps question:", height=100)

if st.button("Get Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        # embed question
        with st.spinner("Finding best match in your notes..."):
            question_emb = embedder.encode([question])
            sims = cosine_similarity(question_emb, chunk_embeddings)
            best_score = sims.max()
            best_idx = sims.argmax()
        
        if best_score > 0.4:
            best_chunk = chunks[best_idx]
            with st.spinner("Answering from notes..."):
                result = qa({
                    "question": question,
                    "context": best_chunk
                })
                answer = result["answer"]
                st.success("Answer from DevOps Notes:")
                for step in answer.split("."):
                    if step.strip():
                        st.write("👉", step.strip())
        else:
            st.info("No good match in your notes. Searching the web...")
            snippets = google_search(question)
            if snippets:
                web_text = " ".join(snippets)
                summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
                with st.spinner("Summarizing Google results..."):
                    summary = summarizer(
                        web_text,
                        max_length=180,
                        min_length=50,
                        do_sample=False
                    )[0]['summary_text']
                    st.success("Answer from Google:")
                    for step in summary.split("."):
                        if step.strip():
                            st.write("👉", step.strip())
            else:
                st.warning("No results from Google either. Try rephrasing your question.")

        st.caption("⚡ Answers are either from your notes or a web search.")

