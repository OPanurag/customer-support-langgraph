import json
from sentence_transformers import SentenceTransformer
import chromadb

# Load local embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.Client()
collection = chroma_client.create_collection("kb_faq")

def load_kb(path="data/kb_faq.json"):
    """Load KB JSON file."""
    with open(path, "r") as f:
        return json.load(f)

def get_embedding(text: str):
    """Generate embedding for a text string."""
    return embedding_model.encode(text).tolist()

def index_kb():
    """Index knowledge base into Chroma."""
    kb = load_kb()
    for entry in kb:
        embedding = get_embedding(entry["question"])
        collection.add(
            ids=[entry["id"]],
            embeddings=[embedding],
            metadatas=[{"answer": entry["answer"]}],
            documents=[entry["question"]],
        )

def query_kb(user_query: str, top_k=2):
    """Query KB with a user question and return top matches."""
    embedding = get_embedding(user_query)
    results = collection.query(query_embeddings=[embedding], n_results=top_k)
    return [
        {"question": doc, "answer": meta["answer"]}
        for doc, meta in zip(results["documents"][0], results["metadatas"][0])
    ]

# Index once on startup
index_kb()
