# src/langie/retriever.py
import chromadb
from chromadb.api.types import EmbeddingFunction
from sentence_transformers import SentenceTransformer

DB_PATH = "data/chroma"
COLLECTION_NAME = "faq"

class SentenceTransformerEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input):
        # input is a list[str]
        return self.model.encode(input).tolist()


class Retriever:
    def __init__(self):
        # Load persisted Chroma
        self.client = chromadb.PersistentClient(path=DB_PATH)

        # Pass in wrapper embedding function
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=SentenceTransformerEmbeddingFunction()
        )

    def search(self, query: str, top_k: int = 3):
        """Search FAQ KB using local embeddings + ChromaDB."""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )

        hits = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            hits.append({
                "question": meta.get("question"),
                "answer": meta.get("answer"),
                "doc": doc
            })
        return hits


if __name__ == "__main__":
    retriever = Retriever()
    res = retriever.search("What is your return policy?")
    for r in res:
        print(f"Q: {r['question']}\nA: {r['answer']}\n")
