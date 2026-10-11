#!/bin/bash

echo "========================================="
echo "       Iniciando Nexus IA (Local)"
echo "========================================="
echo ""

if [ ! -d ".venv" ]; then
    echo "[1/3] Criando ambiente virtual local (.venv)..."
    python3 -m venv .venv
fi

echo "[2/3] Ativando ambiente virtual e verificando dependências..."
echo "Isso pode demorar na primeira vez pois pacotes de IA são grandes."
source .venv/bin/activate

pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Erro ao instalar dependências."
    exit 1
fi
echo "Dependências OK."
echo ""

echo "[3/4] Iniciando Servidor Local de Inteligência (Ollama)..."
curl -s http://localhost:11434/api/tags > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Iniciando o motor do Ollama silenciosamente..."
    ollama serve > /dev/null 2>&1 &
    while ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; do
        sleep 1
    done
fi

echo "[4/4] Iniciando Interface Web..."
streamlit run ui/app.py --browser.gatherUsageStats false
