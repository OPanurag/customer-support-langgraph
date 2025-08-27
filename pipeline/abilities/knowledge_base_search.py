# pipeline/abilities/knowledge_base_search.py
from src.langie.retriever import Retriever

class KnowledgeBaseSearch:
    def __init__(self, config=None):
        # Config may hold db path, collection name, top-k, etc.
        db_path = config.get("db_path", "data/chroma") if config else "data/chroma"
        collection = config.get("collection", "faq") if config else "faq"
        self.top_k = config.get("top_k", 3) if config else 3

        self.retriever = Retriever(db_path=db_path, collection_name=collection)

    def run(self, state: dict):
        query = state.get("input", {}).get("text", "")
        if not query:
            state["knowledge_base"] = []
            return state

        results = self.retriever.query(query, k=self.top_k)

        # Normalize into pipeline output
        state["knowledge_base"] = [
            {
                "id": r["id"],
                "answer": r["text"],  # Chroma stores answer in doc text
                "score": r["score"],
                "metadata": r["metadata"]
            }
            for r in results
        ]
        return state
