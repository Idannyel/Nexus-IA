@echo off
echo =========================================
echo       Iniciando Nexus IA (Local)
echo =========================================
echo.

IF NOT EXIST ".venv\Scripts\activate.bat" (
    echo [1/3] Criando ambiente virtual local venv...
    python -m venv .venv
)

echo [2/3] Ativando ambiente virtual e instalando/verificando dependencias...
echo Isso pode demorar na primeira vez pois pacotes de IA sao grandes.
call .venv\Scripts\activate.bat

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Erro ao instalar dependencias.
    pause
    exit /b %errorlevel%
)
echo Dependencias OK.
echo.

echo [3/4] Iniciando Servidor Local de Inteligencia (Ollama)...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo Iniciando o motor do Ollama silenciosamente...
    start /B ollama serve >nul 2>&1
    :wait_ollama
    timeout /t 1 /nobreak >nul
    curl -s http://localhost:11434/api/tags >nul 2>&1
    if errorlevel 1 goto wait_ollama
)

echo [4/4] Iniciando Interface Web...
streamlit run ui/app.py --browser.gatherUsageStats false

pause
