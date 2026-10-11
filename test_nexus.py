import sys
import os

from core.orchestrator import AgentOrchestrator
from memory.rag_pipeline import RAGPipeline
from tools.shell_tool import ShellTool
from core.llm_engine import LLMEngine

def run_tests():
    print("Testing instantiation...")
    llm = LLMEngine()
    rag = RAGPipeline()
    shell = ShellTool()
    orch = AgentOrchestrator()
    print("All components instantiated successfully.")

    print("Testing LLM mock (Ollama needs to be running for real test)...")
    print("Available models:", llm.get_available_models())
    
    print("Testing Shell Tool...")
    res = shell.execute("echo hello")
    assert "hello" in res.lower()
    print("Shell tool works.")
    
    print("Testing FAISS memory...")
    # Create dummy text
    with open("test_dummy.txt", "w") as f:
        f.write("This is a dummy document for Nexus IA RAG test.")
        
    chunks = rag.index_document("test_dummy.txt")
    print(f"Indexed {chunks} chunks.")
    
    context = rag.query_documents("Nexus IA")
    assert "dummy document" in context
    print("RAG query works.")
    
    os.remove("test_dummy.txt")
    print("ALL TESTS PASSED!")

if __name__ == "__main__":
    run_tests()
