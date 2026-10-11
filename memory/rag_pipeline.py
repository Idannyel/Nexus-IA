import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings
from core.config import settings

class RAGPipeline:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
        self.db_path = settings.VECTOR_DB_DIR
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

    def _get_path(self, collection_name: str) -> str:
        return os.path.join(self.db_path, collection_name)

    def index_document(self, file_path: str, collection_name: str = "documents"):
        """Carrega, divide em chunks e salva no FAISS."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
            
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            loader = PyPDFLoader(file_path)
        elif ext in ['.txt', '.py', '.md']:
            loader = TextLoader(file_path, encoding='utf-8')
        elif ext == '.docx':
            loader = UnstructuredWordDocumentLoader(file_path)
        else:
            raise ValueError(f"Formato não suportado: {ext}")
            
        docs = loader.load()
        chunks = [c for c in self.text_splitter.split_documents(docs) if c.page_content.strip()]
        if not chunks:
            raise ValueError("Nenhum texto extraível encontrado no documento (PDF escaneado/imagem ou arquivo vazio?).")
        
        path = self._get_path(collection_name)
        
        if os.path.exists(path) and os.listdir(path):
            try:
                vectorstore = FAISS.load_local(path, self.embeddings, allow_dangerous_deserialization=True)
                vectorstore.add_documents(chunks)
            except Exception:
                vectorstore = FAISS.from_documents(chunks, self.embeddings)
        else:
            vectorstore = FAISS.from_documents(chunks, self.embeddings)
            os.makedirs(path, exist_ok=True)
            
        vectorstore.save_local(path)
        return len(chunks)
        
    def query_documents(self, query: str, collection_name: str = "documents") -> str:
        """Busca o contexto relevante."""
        path = self._get_path(collection_name)
        if not os.path.exists(path) or not os.listdir(path):
            return ""
            
        try:
            vectorstore = FAISS.load_local(path, self.embeddings, allow_dangerous_deserialization=True)
            docs = vectorstore.similarity_search(query, k=3)
            return "\n\n".join([doc.page_content for doc in docs])
        except Exception:
            return ""

    def delete_document(self, file_path: str, collection_name: str = "documents"):
        """Remove o arquivo físico e reconstrói o índice vetorial com os documentos restantes."""
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass

        path = self._get_path(collection_name)
        if os.path.exists(path):
            import shutil
            shutil.rmtree(path, ignore_errors=True)

        docs_dir = os.path.dirname(file_path) if os.path.dirname(file_path) else "data/documents"
        if os.path.isdir(docs_dir):
            for remaining in sorted(os.listdir(docs_dir)):
                full_path = os.path.join(docs_dir, remaining)
                if os.path.isfile(full_path):
                    try:
                        self.index_document(full_path, collection_name)
                    except Exception:
                        pass

    def clear_all_documents(self, docs_dir: str = "data/documents", collection_name: str = "documents"):
        """Apaga todos os documentos físicos e zera o índice vetorial."""
        if os.path.isdir(docs_dir):
            for f in os.listdir(docs_dir):
                p = os.path.join(docs_dir, f)
                if os.path.isfile(p):
                    try:
                        os.remove(p)
                    except Exception:
                        pass

        path = self._get_path(collection_name)
        if os.path.exists(path):
            import shutil
            shutil.rmtree(path, ignore_errors=True)
