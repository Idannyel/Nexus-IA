import streamlit as st
import sys
import os
import base64
from urllib.parse import urlparse
from PIL import Image, ImageDraw

# Ensure modules from parent directory can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.orchestrator import AgentOrchestrator
from core.llm_engine import LLMEngine
from core.config import settings
from memory.rag_pipeline import RAGPipeline
from icons import svg
import importlib
import styles
importlib.reload(styles)
from styles import build_css

UI_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(UI_DIR, "icon.ico")            # logo original (favicon)
LOGO_PATH = os.path.join(UI_DIR, "assets", "logo.png")  # logo original em PNG (sem alteração visual)


def _ensure_logo_png():
    """Gera o PNG a partir do icon.ico (maior resolução) somente se ainda não existir."""
    if os.path.exists(LOGO_PATH):
        return
    os.makedirs(os.path.dirname(LOGO_PATH), exist_ok=True)
    ico = Image.open(ICON_PATH)
    sizes = sorted(ico.info.get("sizes", [ico.size]))
    ico.size = max(sizes)
    ico.convert("RGBA").save(LOGO_PATH)


_ensure_logo_png()
im = Image.open(ICON_PATH)
LOGO_IMG = Image.open(LOGO_PATH)
with open(LOGO_PATH, "rb") as _f:
    LOGO_SRC = "data:image/png;base64," + base64.b64encode(_f.read()).decode()

st.set_page_config(
    page_title="Nexus IA - Local Agent",
    page_icon=im,
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(build_css(), unsafe_allow_html=True)


@st.cache_resource
def get_orchestrator():
    return AgentOrchestrator()

@st.cache_resource
def get_llm():
    return LLMEngine()

@st.cache_resource
def get_rag():
    return RAGPipeline()

orchestrator = get_orchestrator()
llm = get_llm()
rag = get_rag()

PAGES = ["Chat", "Configurações", "Arquivos", "Modelos", "Sobre"]

# O indicador de privacidade reflete a configuração real: Ollama em host local?
_host = (urlparse(settings.OLLAMA_BASE_URL).hostname or "").lower()
IS_LOCAL = _host in ("localhost", "127.0.0.1", "::1")

# Barra lateral
with st.sidebar:
    st.markdown(
        f'<div class="nx-brand"><img src="{LOGO_SRC}" alt="Nexus IA"/>'
        '<div class="nx-brand-name">Nexus <b>IA</b></div></div>',
        unsafe_allow_html=True,
    )
    page = st.radio("Navegação", PAGES, key="page", label_visibility="collapsed")

    with st.container(border=True):
        st.markdown(f'<div class="nx-ptitle">{svg("settings", 16)}Configurações do Modelo</div>', unsafe_allow_html=True)

        # Model Selection
        available_models = llm.get_available_models()
        if not available_models:
            st.error("Nenhum modelo encontrado! Certifique-se de baixar um modelo no Ollama (ex: 'ollama run gemma3').")
            st.stop()
        selected_model = st.selectbox("Modelo Local (Ollama)", available_models, index=0)
        settings.DEFAULT_MODEL = selected_model

        # Persona Selection
        selected_persona = st.selectbox("Personalidade", list(settings.PERSONAS.keys()))

        # Tool Toggles
        st.markdown('<div class="nx-label">Capacidades</div>', unsafe_allow_html=True)
        use_rag = st.checkbox("Memória / Documentos (RAG)", value=True)
        use_tools = st.checkbox("Ferramentas (Shell)", value=True, help="Use /shell [cmd]")

        if st.button("Limpar Chat"):
            st.session_state.messages = []
            st.rerun()

    with st.container(border=True):
        st.markdown(f'<div class="nx-ptitle">{svg("database", 16)}Base de Conhecimento</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload PDF/TXT", type=['pdf', 'txt', 'md', 'docx'])
        if uploaded_file:
            # Save temp file
            os.makedirs("data/documents", exist_ok=True)
            file_path = os.path.join("data/documents", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            file_key = f"{uploaded_file.name}:{uploaded_file.size}"
            if st.session_state.get("indexed_file") != file_key:
                with st.spinner("Indexando..."):
                    try:
                        chunks = rag.index_document(file_path)
                        st.session_state["indexed_file"] = file_key
                        st.success(f"Arquivo indexado! ({chunks} chunks)")
                    except Exception as e:
                        st.error(f"Falha ao indexar: {e}")
            else:
                st.info("Arquivo já indexado.")

# Barra superior
st.markdown(
    '<div class="nx-top">'
    f'<span class="nx-pill{"" if IS_LOCAL else " off"}"><span class="dot"></span>'
    f'{"100% local · privado" if IS_LOCAL else "Servidor externo"}</span>'
    '</div>',
    unsafe_allow_html=True,
)


def _kv(rows):
    cells = "".join(f'<div class="k">{k}</div><div>{v}</div>' for k, v in rows)
    return f'<div class="nx-kv">{cells}</div>'


def render_hero():
    cards = [
        ("shield", "Privacidade total", "Seus dados são seus."),
        ("zap", "Rápido e eficiente", "Resposta em segundos."),
        ("box", "Modelo local", "Ollama + Gemma3."),
        ("brain", "Multifuncional", "Com memória e ferramentas."),
    ]
    cards_html = "".join(
        f'<div class="nx-card"><div class="ico">{svg(i, 22)}</div>'
        f'<div><div class="t">{t}</div><div class="d">{d}</div></div></div>'
        for i, t, d in cards
    )
    st.markdown(
        '<div class="nx-welcome-wrap">'
        f'<div class="nx-hero"><img src="{LOGO_SRC}" alt="Nexus IA"/>'
        '<h1>Nexus <b>IA</b></h1>'
        '<p>Assistente corporativo autônomo. Seus dados permanecem na sua máquina.</p></div>'
        f'<div class="nx-cards">{cards_html}</div>'
        '<div class="nx-greet-wrap">'
        '<div class="nx-greet">Olá! Como posso te ajudar <b>hoje?</b></div>'
        '<div class="nx-greet-sub">Faça uma pergunta, peça uma análise, gere um documento ou use as '
        'ferramentas para resolver o que precisar.</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )


def render_settings():
    st.markdown(
        '<div class="nx-page"><h2>Configurações</h2><div class="sub">Estado atual do agente (edite as opções na barra lateral).</div></div>'
        + _kv([
            ("Modelo ativo", selected_model),
            ("Personalidade", selected_persona),
            ("Memória / Documentos (RAG)", "Ativada" if use_rag else "Desativada"),
            ("Ferramentas (Shell)", "Ativadas" if use_tools else "Desativadas"),
            ("Servidor Ollama", settings.OLLAMA_BASE_URL),
            ("Privacidade", "Processamento 100% local · dados confidenciais" if IS_LOCAL else "Servidor remoto configurado"),
        ]),
        unsafe_allow_html=True,
    )


def render_files():
    docs_dir = os.path.join("data", "documents")
    files = sorted([f for f in os.listdir(docs_dir) if not f.startswith(".") and f != ".keep"]) if os.path.isdir(docs_dir) else []

    st.markdown(
        '<div class="nx-page">'
        '<h2>Arquivos</h2>'
        '<div class="sub">Documentos sincronizados na base de conhecimento local para RAG.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    if not files:
        st.markdown(
            '<div class="nx-empty">'
            f'<div class="nx-empty-ico">{svg("file", 32)}</div>'
            '<div class="nx-empty-title">Nenhum documento na base de conhecimento</div>'
            '<div class="nx-empty-desc">Envie arquivos PDF, TXT, DOCX ou MD através da barra lateral para indexar e consultar via RAG.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    total_bytes = sum(os.path.getsize(os.path.join(docs_dir, f)) for f in files)
    total_str = f"{total_bytes / 1024:.1f} KB" if total_bytes < 1024 * 1024 else f"{total_bytes / (1024 * 1024):.2f} MB"
    plural = "s" if len(files) > 1 else ""

    col_meta, col_bulk = st.columns([4.8, 1.2])
    with col_meta:
        st.markdown(
            f'<div class="nx-files-header-meta">'
            f'<span class="nx-dot-ok"></span>'
            f'<span><b>{len(files)}</b> documento{plural} indexado{plural} &middot; {total_str} no total</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with col_bulk:
        if len(files) > 1:
            if st.button("Limpar todos", key="btn_clear_all_files", use_container_width=True):
                rag.clear_all_documents(docs_dir=docs_dir)
                st.session_state.pop("indexed_file", None)
                st.toast("Base de conhecimento zerada.")
                st.rerun()

    st.markdown('<div class="nx-files-divider"></div>', unsafe_allow_html=True)

    for idx, f in enumerate(files):
        size_b = os.path.getsize(os.path.join(docs_dir, f))
        size_str = f"{size_b / 1024:.1f} KB" if size_b < 1024 * 1024 else f"{size_b / (1024 * 1024):.2f} MB"

        col_item, col_act = st.columns([5.2, 1.1])
        with col_item:
            st.markdown(
                f'<div class="nx-file-card">'
                f'<span class="nx-file-card-ico">{svg("file", 18)}</span>'
                f'<div class="nx-file-card-text">'
                f'<span class="nx-file-card-name" title="{f}">{f}</span>'
                f'<span class="nx-file-card-size">{size_str}</span>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with col_act:
            if st.button("Excluir", key=f"del_file_{idx}", use_container_width=True):
                rag.delete_document(os.path.join(docs_dir, f))
                st.session_state.pop("indexed_file", None)
                st.toast(f"'{f}' excluído da base.")
                st.rerun()


def render_models():
    if available_models:
        items = "".join(
            f'<div class="nx-file-row">'
            f'<div class="nx-file-left"><span class="nx-file-ico">{svg("box", 18)}</span><span class="nx-file-name">{m}</span></div>'
            f'{"<span class=\'nx-pill\'><span class=\'dot\'></span>ativo</span>" if m == selected_model else "<span style=\'color:var(--nx-text-3); font-size:var(--nx-fs-xs);\'>disponível</span>"}'
            f'</div>'
            for m in available_models
        )
        body = f'<div class="nx-files-list">{items}</div>'
    else:
        body = '<div class="nx-empty">Nenhum modelo baixado no Ollama. Execute "ollama run gemma3" no terminal.</div>'
    st.markdown(
        '<div class="nx-page"><h2>Modelos</h2><div class="sub">Modelos locais instalados no Ollama.</div></div>' + body,
        unsafe_allow_html=True,
    )


def render_about():
    st.markdown(
        '<div class="nx-page"><h2>Sobre</h2><div class="sub">Nexus IA é um assistente autônomo corporativo que opera localmente via Ollama, '
        'com memória vetorial de documentos (RAG) e ferramentas seguras de terminal.</div></div>'
        + _kv([
            ("Aplicação", "Nexus IA - Local Corporate Agent"),
            ("Motor de IA", "Ollama"),
            ("Formatos suportados", "PDF, TXT, MD, DOCX"),
            ("Armazenamento vetorial", "ChromaDB (local)"),
            ("Dados e Privacidade", "100% privados na sua máquina local" if IS_LOCAL else "Servidor remoto configurado"),
        ]),
        unsafe_allow_html=True,
    )


AVATARS = {"assistant": LOGO_IMG}

if page == "Chat":
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Lê o input do usuário. Se uma nova mensagem foi enviada, registramos antes de decidir a tela.
    prompt = st.chat_input("Como posso ajudar hoje? (Use /shell para executar no terminal)")
    new_user_message = None
    if prompt:
        new_user_message = prompt
        st.session_state.messages.append({"role": "user", "content": prompt})

    # Remove mensagens em branco
    st.session_state.messages = [m for m in st.session_state.messages if m["content"].strip()]

    # Se não há mensagens no histórico, renderiza o Hero / Boas-vindas
    if not st.session_state.messages:
        render_hero()
    else:
        st.markdown('<div class="nx-spacer"></div>', unsafe_allow_html=True)
        # Renderiza todo o histórico prévio (exceto a mensagem recém-submetida que será renderizada abaixo)
        existing_messages = st.session_state.messages[:-1] if new_user_message else st.session_state.messages
        for message in existing_messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(f'<span class="nx-u"></span>' + message["content"], unsafe_allow_html=True)
            else:
                with st.chat_message("assistant", avatar=AVATARS["assistant"]):
                    st.markdown(f'<span class="nx-a"></span>' + message["content"], unsafe_allow_html=True)

        # Se há uma nova mensagem de usuário nesta rodada, exibe e gera a resposta via streaming
        if new_user_message:
            with st.chat_message("user"):
                st.markdown(f'<span class="nx-u"></span>' + new_user_message, unsafe_allow_html=True)

            with st.chat_message("assistant", avatar=AVATARS["assistant"]):
                message_placeholder = st.empty()
                message_placeholder.markdown('<span class="nx-a"></span><div class="nx-typing"><span></span><span></span><span></span></div>', unsafe_allow_html=True)
                full_response = ""

                history_for_llm = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages[:-1]
                    if m["content"].strip()
                ][-5:]

                try:
                    for chunk in orchestrator.process_message(
                        user_message=new_user_message,
                        history=history_for_llm,
                        persona=selected_persona,
                        use_rag=use_rag,
                        use_tools=use_tools
                    ):
                        full_response += chunk
                        message_placeholder.markdown(f'<span class="nx-a"></span>' + full_response + "▌", unsafe_allow_html=True)
                    if full_response.strip():
                        message_placeholder.markdown(f'<span class="nx-a"></span>' + full_response, unsafe_allow_html=True)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    else:
                        message_placeholder.warning("O modelo não retornou resposta. Tente novamente ou escolha outro modelo.")
                except Exception as e:
                    st.error(f"Erro ao comunicar com o LLM local. Certifique-se de que o Ollama está rodando. Detalhes: {str(e)}")

elif page == "Configurações":
    render_settings()
elif page == "Arquivos":
    render_files()
elif page == "Modelos":
    render_models()
else:
    render_about()

