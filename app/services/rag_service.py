import os
import glob
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.utils.config import DATA_KNOWLEDGE
from app.utils.logger import app_logger

class HRPolicyRAGEngine:
    _instance = None
    
    def __init__(self):
        self.documents = []
        self.chunks = []
        self.vectorizer = None
        self.tfidf_matrix = None
        self._build_index()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _build_index(self):
        md_files = glob.glob(os.path.join(DATA_KNOWLEDGE, "*.md"))
        app_logger.info(f"Indexing {len(md_files)} HR policy documents for RAG...")
        
        self.chunks = []
        for fpath in md_files:
            fname = os.path.basename(fpath)
            with open(fpath, "r", encoding="utf-8") as f:
                text = f.read()
            
            # Split by markdown headers
            sections = re.split(r'\n(?=###?\s+)', text)
            for sec in sections:
                cleaned = sec.strip()
                if len(cleaned) > 20:
                    self.chunks.append({
                        "source": fname,
                        "content": cleaned
                    })
        
        corpus = [c["content"] for c in self.chunks]
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        app_logger.info(f"Built TF-IDF RAG index with {len(self.chunks)} knowledge chunks.")

    def search(self, query: str, top_k: int = 3):
        if not self.chunks:
            return {"query": query, "answer": "No policy documents found in knowledge repository.", "retrieved_sources": []}
        
        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        top_indices = sims.argsort()[::-1][:top_k]
        
        retrieved = []
        for idx in top_indices:
            score = float(sims[idx])
            if score > 0.05:
                retrieved.append({
                    "source": self.chunks[idx]["source"],
                    "score": round(score, 4),
                    "snippet": self.chunks[idx]["content"]
                })
                
        if not retrieved:
            answer = "I could not find a specific HR policy section addressing that query in the corporate handbook. Please contact HR Operations."
        else:
            primary = retrieved[0]
            answer = f"**Grounded HR Policy Answer (Source: {primary['source']}):**\n\n{primary['snippet']}"
            
        return {
            "query": query,
            "answer": answer,
            "retrieved_sources": retrieved
        }
