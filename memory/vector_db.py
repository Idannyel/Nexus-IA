import os
from langchain_community.vectorstores import FAISS
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings
from core.config import settings

class MemoryDB:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
        self.db_path = settings.VECTOR_DB_DIR
        
    def _get_path(self, collection_name: str) -> str:
        return os.path.join(self.db_path, collection_name)
    
    def add_memory(self, text: str, metadata: dict = None, collection_name: str = "long_term_memory"):
        path = self._get_path(collection_name)
        
        # Meta default
        if not metadata:
            metadata = {"source": "chat"}
            
        if os.path.exists(path) and os.listdir(path):
            try:
                vectorstore = FAISS.load_local(path, self.embeddings, allow_dangerous_deserialization=True)
                vectorstore.add_texts(texts=[text], metadatas=[metadata])
            except Exception:
                vectorstore = FAISS.from_texts(texts=[text], embedding=self.embeddings, metadatas=[metadata])
        else:
            vectorstore = FAISS.from_texts(texts=[text], embedding=self.embeddings, metadatas=[metadata])
            os.makedirs(path, exist_ok=True)
            
        vectorstore.save_local(path)
        return "saved"
        
    def search_memory(self, query: str, n_results: int = 3, collection_name: str = "long_term_memory"):
        path = self._get_path(collection_name)
        if not os.path.exists(path) or not os.listdir(path):
            return []
            
        try:
            vectorstore = FAISS.load_local(path, self.embeddings, allow_dangerous_deserialization=True)
            docs = vectorstore.similarity_search(query, k=n_results)
            return [doc.page_content for doc in docs]
        except Exception:
            return []
