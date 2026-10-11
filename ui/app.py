import streamlit as st
import sys
import os
import re
import base64
from urllib.parse import urlparse
from PIL import Image

# Ensure modules from parent directory can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.orchestrator import AgentOrchestrator
from core.llm_engine import LLMEngine
from core.config import settings
from core.model_manager import model_manager, MODEL_CATALOG
from memory.rag_pipeline import RAGPipeline
from icons import svg
import importlib
import styles
importlib.reload(styles)
from styles import build_css

UI_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(UI_DIR, "icon.ico")
LOGO_PATH = os.path.join(UI_DIR, "assets", "logo.png")


def _ensure_logo_png():
    """Gera o PNG a partir do icon.ico somente se ainda não existir."""
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

# Indicador de privacidade local
_host = (urlparse(settings.OLLAMA_BASE_URL).hostname or "").lower()
IS_LOCAL = _host in ("localhost", "127.0.0.1", "::1")


def _execute_download(model_tag: str, container=None):
    """Executa o download de um modelo via streaming com barra de progresso visual."""
    ctx = container or st
    progress_bar = ctx.progress(0)
    status_box = ctx.empty()
    status_box.info(f"Iniciando download do modelo '{model_tag}' via Ollama...")

    try:
        for event in model_manager.pull_model_stream(model_tag):
            st_text = event.get("status", "")
            percent = float(event.get("percent", 0.0))
            completed_mb = event.get("completed_mb", 0.0)
            total_mb = event.get("total_mb", 0.0)

            if event.get("status") == "error":
                status_box.error(event.get("message", "Erro no download."))
                return
            elif event.get("status") == "success":
                progress_bar.progress(100)
                status_box.success(event.get("message", "Download concluído!"))
                st.session_state.active_model = model_tag
                settings.DEFAULT_MODEL = model_tag
                st.rerun()
                return
            else:
                pct_norm = max(0.0, min(percent / 100.0, 1.0))
                progress_bar.progress(pct_norm)
                detail = f" — {completed_mb:.1f} MB / {total_mb:.1f} MB" if total_mb > 0 else ""
                status_box.text(f"{st_text}{detail} ({percent:.1f}%)")
    except Exception as e:
        status_box.error(f"Falha durante o download: {str(e)}")


# Inicialização do estado de sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Verificação do status do Ollama e modelos instalados
ollama_online = model_manager.is_available()
installed_models_data = model_manager.list_installed_models() if ollama_online else []
installed_tags = [m["name"] for m in installed_models_data]

# Lista de modelos efetivamente instalados no Ollama para seleção direta
selectable_models = list(installed_tags)

# Sincronização do modelo ativo
if "active_model" not in st.session_state or not st.session_state.active_model or st.session_state.active_model not in selectable_models:
    if settings.DEFAULT_MODEL in selectable_models:
        st.session_state.active_model = settings.DEFAULT_MODEL
    elif selectable_models:
        st.session_state.active_model = selectable_models[0]
    else:
        st.session_state.active_model = None

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

        if not ollama_online:
            st.warning("Serviço Ollama não detectado em localhost:11434. Inicie o Ollama no terminal com 'ollama serve'.")
            selected_model = None
        elif not selectable_models:
            st.warning("Nenhum modelo baixado localmente no Ollama. Acesse a página 'Modelos' para baixar uma IA.")
            selected_model = None
        else:
            def format_sidebar_model(tag: str) -> str:
                fam = model_manager.detect_family(tag)
                fam_info = model_manager.get_family_info(fam)
                fam_name = fam_info.get("name", fam.capitalize())

                size_str = ""
                for m in installed_models_data:
                    if m["name"] == tag:
                        size_str = f" ({m['size_gb']:.1f} GB)"
                        break

                return f"{tag} · {fam_name}{size_str}"

            cur_idx = selectable_models.index(st.session_state.active_model) if st.session_state.active_model in selectable_models else 0
            selected_model = st.selectbox(
                "Modelo Local",
                selectable_models,
                index=cur_idx,
                format_func=format_sidebar_model,
                key="sidebar_model_select"
            )
            st.session_state.active_model = selected_model
            settings.DEFAULT_MODEL = selected_model

            # Badge informativa da família e estado do modelo ativo
            fam = model_manager.detect_family(selected_model)
            fam_info = model_manager.get_family_info(fam)

            st.markdown(
                f'<div class="nx-sidebar-model-badge">'
                f'<span class="nx-badge-tag">{fam_info.get("badge", "Ativo")}</span>'
                f'<span class="nx-badge-name">Família: {fam.capitalize()}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

        # Persona Selection
        selected_persona = st.selectbox("Personalidade", list(settings.PERSONAS.keys()))

        # Capacidades
        st.markdown('<div class="nx-label">Capacidades</div>', unsafe_allow_html=True)
        use_rag = st.checkbox("Memória / Documentos (RAG)", value=True)
        use_tools = st.checkbox("Ferramentas (Shell)", value=True, help="Use /shell [cmd]")

        col_clr, col_rel = st.columns(2, gap="small")
        with col_clr:
            if st.button("Limpar Chat", key="sb_btn_clear_chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        with col_rel:
            if st.button("Liberar RAM", key="sb_btn_unload_ram", use_container_width=True):
                if st.session_state.active_model and model_manager.is_model_installed(st.session_state.active_model):
                    model_manager.unload_model(st.session_state.active_model)
                    st.toast(f"Modelo '{st.session_state.active_model}' descarregado da RAM.")

    with st.container(border=True):
        st.markdown(f'<div class="nx-ptitle">{svg("database", 16)}Base de Conhecimento</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload PDF/TXT", type=['pdf', 'txt', 'md', 'docx'])
        if uploaded_file:
            os.makedirs("data/documents", exist_ok=True)
            file_path = os.path.join("data/documents", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            file_key = f"{uploaded_file.name}:{uploaded_file.size}"
            if st.session_state.get("indexed_file") != file_key:
                with st.spinner("Indexando documento..."):
                    try:
                        chunks = rag.index_document(file_path)
                        st.session_state["indexed_file"] = file_key
                        st.success(f"Arquivo indexado! ({chunks} chunks)")
                    except Exception as e:
                        st.error(f"Falha ao indexar: {e}")
            else:
                st.info("Arquivo já indexado.")

# Barra superior com modelo ativo e status local
active_pill_text = st.session_state.active_model or "Sem modelo"
st.markdown(
    '<div class="nx-top">'
    f'<span class="nx-pill"><span class="dot"></span>{active_pill_text}</span>'
    f'<span class="nx-pill{"" if (IS_LOCAL and ollama_online) else " off"}"><span class="dot"></span>'
    f'{"100% local · privado" if (IS_LOCAL and ollama_online) else ("Ollama desconectado" if not ollama_online else "Servidor externo")}</span>'
    '</div>',
    unsafe_allow_html=True,
)


def _kv(rows):
    cells = "".join(f'<div class="k">{k}</div><div>{v}</div>' for k, v in rows)
    return f'<div class="nx-kv">{cells}</div>'


def format_chat_text(content: str) -> str:
    """Formata tags de raciocínio como <think> (DeepSeek-R1 e modelos analíticos) em blocos visuais estilizados."""
    if not content:
        return ""

    def _replace_think(match):
        thought = match.group(1).strip()
        return (
            f'<details class="nx-think-details" open>'
            f'<summary class="nx-think-title">{svg("brain", 14)} Raciocínio Analítico</summary>'
            f'<div class="nx-think-body">{thought}</div>'
            f'</details>'
        )

    formatted = re.sub(r"<think>(.*?)</think>", _replace_think, content, flags=re.DOTALL)

    if "<think>" in formatted and "</think>" not in formatted:
        parts = formatted.split("<think>", 1)
        formatted = (
            f'{parts[0]}<details class="nx-think-details" open>'
            f'<summary class="nx-think-title">{svg("brain", 14)} Raciocínio em andamento...</summary>'
            f'<div class="nx-think-body">{parts[1]}</div>'
            f'</details>'
        )

    return formatted


def render_hero():
    cards = [
        ("shield", "Privacidade total", "Seus dados permanecem na sua máquina local."),
        ("cpu", "Plataforma Multimodelo", "Alterne livremente entre Llama, Gemma, DeepSeek, Dolphin e outros."),
        ("database", "Memória & RAG", "Indexação local de documentos (PDF, TXT, MD, DOCX)."),
        ("terminal", "Ferramentas Locais", "Execução segura de comandos no terminal via /shell."),
    ]
    cards_html = "".join(
        f'<div class="nx-card"><div class="ico">{svg(i, 22)}</div>'
        f'<div class="cnt"><div class="t">{t}</div><div class="d">{d}</div></div></div>'
        for i, t, d in cards
    )
    st.markdown(
        '<div class="nx-welcome-wrap">'
        f'<div class="nx-hero"><img src="{LOGO_SRC}" alt="Nexus IA"/>'
        '<h1>Nexus <b>IA</b></h1>'
        '<p>Assistente corporativo autônomo com suporte multimodelo e execução 100% local privada.</p></div>'
        f'<div class="nx-cards">{cards_html}</div>'
        '<div class="nx-greet-wrap">'
        '<div class="nx-greet">Olá! Como posso te ajudar <b>hoje?</b></div>'
        '<div class="nx-greet-sub">Faça uma pergunta, solicite uma análise de código, explore documentos ou utilize comandos no terminal.</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )


def render_settings():
    active_m = st.session_state.active_model or "Nenhum selecionado"
    active_params = model_manager.get_model_params(active_m) if active_m else {}

    st.markdown(
        '<div class="nx-page"><h2>Configurações</h2><div class="sub">Estado atual do sistema e parâmetros de geração.</div></div>'
        + _kv([
            ("Modelo ativo", active_m),
            ("Personalidade", selected_persona),
            ("Temperatura ativa", str(active_params.get("temperature", 0.7))),
            ("Limite de tokens", str(active_params.get("num_predict", 2048))),
            ("Top-P", str(active_params.get("top_p", 0.9))),
            ("Memória / Documentos (RAG)", "Ativada" if use_rag else "Desativada"),
            ("Ferramentas (Shell)", "Ativadas" if use_tools else "Desativadas"),
            ("Servidor Ollama", settings.OLLAMA_BASE_URL),
            ("Privacidade", "Processamento 100% local · dados confidenciais" if IS_LOCAL else "Servidor remoto"),
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
    st.markdown(
        '<div class="nx-page">'
        '<h2>Central de Modelos de IA</h2>'
        '<div class="sub">Gerenciamento unificado de modelos locais, compatibilidade de hardware e controle de inferência via Ollama.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # 1. Diagnóstico de Hardware Local
    hw = model_manager.get_hardware_info()
    ollama_status_text = "Online (localhost:11434)" if ollama_online else "Indisponível (inicie 'ollama serve')"
    gpu_label = hw["gpu_name"] + (f" ({hw['vram_gb']} GB VRAM)" if hw["vram_gb"] > 0 else "")
    ollama_dot = '<span class="nx-dot-ok"></span>' if ollama_online else '<span class="nx-dot-err"></span>'

    st.markdown(
        f'<div class="nx-section-header first">'
        f'<div class="nx-section-title">{svg("cpu", 16)} Diagnóstico de Hardware & Status Local</div>'
        f'<div class="nx-section-sub">Recursos computacionais disponíveis e estado do serviço Ollama na máquina.</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="nx-hw-grid">'
        f'<div class="nx-hw-card">'
        f'<div class="nx-hw-title">{svg("cpu", 14)} Memória RAM</div>'
        f'<div class="nx-hw-val">{hw["avail_ram_gb"]:.1f} GB <span class="unit">livres</span></div>'
        f'<div class="nx-hw-sub">Total físico: {hw["total_ram_gb"]:.1f} GB</div>'
        f'</div>'
        f'<div class="nx-hw-card">'
        f'<div class="nx-hw-title">{svg("hard-drive", 14)} Armazenamento Ollama</div>'
        f'<div class="nx-hw-val">{hw["free_disk_gb"]:.1f} GB <span class="unit">livres</span></div>'
        f'<div class="nx-hw-sub" title="{hw.get("ollama_path", "Local")}">Disco ({hw.get("ollama_path", "Local")})</div>'
        f'</div>'
        f'<div class="nx-hw-card">'
        f'<div class="nx-hw-title">{svg("zap", 14)} Acelerador Gráfico</div>'
        f'<div class="nx-hw-val" title="{gpu_label}">{gpu_label}</div>'
        f'<div class="nx-hw-sub">Inferência quantizada local (GPU)</div>'
        f'</div>'
        f'<div class="nx-hw-card">'
        f'<div class="nx-hw-title">{svg("shield", 14)} Motor Ollama</div>'
        f'<div class="nx-hw-val">{"Ativo" if ollama_online else "Desconectado"}</div>'
        f'<div class="nx-hw-sub">{ollama_dot} {ollama_status_text}</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if not ollama_online:
        st.error(
            "O serviço do Ollama não está em execução ou não respondeu na porta 11434. "
            "Abra o terminal e execute 'ollama serve' para iniciar o motor local."
        )
        if st.button("Tentar Reconectar ao Ollama"):
            st.rerun()
        return

    # 2. Modelos Instalados no Computador
    installed = model_manager.list_installed_models()
    inst_count = len(installed)
    badge_count = f'<span class="nx-count-badge">{inst_count} modelo{"s" if inst_count != 1 else ""}</span>'

    st.markdown(
        f'<div class="nx-section-header">'
        f'<div class="nx-section-title">{svg("box", 16)} Modelos Instalados no Computador {badge_count}</div>'
        f'<div class="nx-section-sub">Modelos baixados localmente prontos para uso offline imediato sem latência de rede.</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if not installed:
        st.markdown(
            '<div class="nx-empty">'
            f'<div class="nx-empty-ico">{svg("box", 32)}</div>'
            '<div class="nx-empty-title">Nenhum modelo baixado no Ollama</div>'
            '<div class="nx-empty-desc">Selecione uma IA no catálogo abaixo e instale-a diretamente no computador.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        for m in installed:
            is_active = (m["name"] == st.session_state.active_model)
            fam = model_manager.detect_family(m["name"])
            fam_badge = MODEL_CATALOG.get(fam, {}).get("badge", "Geral")
            active_class = " active" if is_active else ""
            active_chip = "<span class='nx-tag-chip accent'><span class='nx-dot-ok' style='margin-right:4px;'></span>Ativo</span>" if is_active else ""

            card_html = (
                f'<div class="nx-model-table-card{active_class}">'
                f'<div class="nx-model-table-left">'
                f'<span class="nx-model-table-ico">{svg("box", 16)}</span>'
                f'<div class="nx-model-table-meta">'
                f'<span class="nx-model-table-name" title="{m["name"]}">{m["name"]}</span>'
                f'{active_chip}'
                f'</div>'
                f'</div>'
                f'<div class="nx-model-table-tags">'
                f'<span class="nx-tag-chip">{m["size_gb"]:.2f} GB</span>'
                f'<span class="nx-tag-chip">{fam.capitalize()}</span>'
                f'<span class="nx-tag-chip">{fam_badge}</span>'
                f'</div>'
                f'</div>'
            )

            # Mantém a mesma proporção total (5.0 + 2.4 = 7.4) para alinhamento horizontal perfeitamente unificado
            if is_active:
                col_info, col_b1 = st.columns([5.0, 2.4], gap="medium")
                with col_info:
                    st.markdown(card_html, unsafe_allow_html=True)
                with col_b1:
                    if st.button("Liberar RAM", key=f"tbl_unl_{m['name']}", use_container_width=True):
                        model_manager.unload_model(m["name"])
                        st.toast(f"'{m['name']}' descarregado da memória RAM.")
            else:
                col_info, col_b1, col_b2 = st.columns([5.0, 1.3, 1.1], gap="medium")
                with col_info:
                    st.markdown(card_html, unsafe_allow_html=True)
                with col_b1:
                    if st.button("Ativar", key=f"tbl_act_{m['name']}", use_container_width=True):
                        st.session_state.active_model = m["name"]
                        settings.DEFAULT_MODEL = m["name"]
                        st.rerun()
                with col_b2:
                    if st.button("Excluir", key=f"tbl_del_{m['name']}", use_container_width=True):
                        model_manager.delete_model(m["name"])
                        st.toast(f"'{m['name']}' excluído do computador.")
                        st.rerun()

    # 3. Instalar Nova IA Diretamente no Computador
    st.markdown(
        f'<div class="nx-section-header">'
        f'<div class="nx-section-title">{svg("download", 16)} Instalar Nova IA no Computador</div>'
        f'<div class="nx-section-sub">Download e quantização executados diretamente no computador com verificação de hardware.</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        col_cat_fam, col_cat_var = st.columns([1, 1], gap="large")
        with col_cat_fam:
            catalog_families = [k for k in MODEL_CATALOG.keys() if k != "general"]
            family_labels = {k: f"{MODEL_CATALOG[k]['name']} ({MODEL_CATALOG[k]['badge']})" for k in catalog_families}
            family_labels["custom"] = "Digitar tag manual do Ollama..."

            family_options = catalog_families + ["custom"]
            chosen_family = st.selectbox(
                "Família de IA:",
                family_options,
                format_func=lambda k: family_labels.get(k, k),
                key="install_fam_select",
            )

        model_tag_to_install = None
        est_size_gb = 2.0
        est_ram_gb = 4.0
        var_desc = ""
        var_badge = "Geral"

        with col_cat_var:
            if chosen_family == "custom":
                custom_tag = st.text_input(
                    "Tag do modelo no Ollama:",
                    placeholder="ex: qwen2.5:3b, mistral:7b, phi3:mini",
                    key="install_custom_tag",
                )
                model_tag_to_install = custom_tag.strip()
                est_size_gb = 2.5
                est_ram_gb = 4.0
                var_desc = "Modelo customizado informado pelo usuário diretamente do repositório Ollama."
                var_badge = "Custom"
            else:
                cat_data = MODEL_CATALOG[chosen_family]
                variants = cat_data.get("variants", [])
                if variants:
                    var_labels = [f"{v['tag']} — {v['size_gb']} GB ({v['badge']})" for v in variants]
                    var_idx = st.selectbox(
                        "Variante do Modelo:",
                        range(len(variants)),
                        format_func=lambda i: var_labels[i],
                        key="install_var_select",
                    )
                    selected_var = variants[var_idx]
                    model_tag_to_install = selected_var["tag"]
                    est_size_gb = selected_var["size_gb"]
                    est_ram_gb = selected_var["min_ram_gb"]
                    var_desc = selected_var.get("description", "")
                    var_badge = selected_var.get("badge", "Padrão")
                else:
                    st.info("Nenhuma variante pré-configurada nesta categoria.")

        # Card de Especificação e Diagnóstico Pré-Instalação
        if model_tag_to_install:
            is_already_installed = model_manager.is_model_installed(model_tag_to_install)
            compat = model_manager.evaluate_compatibility(est_size_gb, est_ram_gb)

            st.markdown(
                f'<div class="nx-spec-badge-bar">'
                f'<span class="nx-spec-badge-item"><strong>Tag:</strong> <code>{model_tag_to_install}</code></span>'
                f'<span class="nx-spec-badge-item">&bull; <strong>Download:</strong> ~{est_size_gb:.1f} GB</span>'
                f'<span class="nx-spec-badge-item">&bull; <strong>RAM Mínima:</strong> {est_ram_gb:.1f} GB</span>'
                f'<span class="nx-spec-badge-item">&bull; <strong>Perfil:</strong> {var_badge}</span>'
                + (f'<div class="nx-spec-desc-text">{var_desc}</div>' if var_desc else "")
                + f'</div>',
                unsafe_allow_html=True,
            )

            col_c_msg, col_c_btn = st.columns([3.8, 1.8], gap="medium")
            with col_c_msg:
                if is_already_installed:
                    st.success(f"O modelo '{model_tag_to_install}' já está instalado no computador e pronto para uso.")
                elif compat["status"] == "error":
                    st.error(compat["message"])
                elif compat["status"] == "warning":
                    st.warning(compat["message"])
                else:
                    st.info(compat["message"])

            with col_c_btn:
                if is_already_installed:
                    if st.session_state.active_model == model_tag_to_install:
                        st.markdown(
                            '<div class="nx-already-active-btn">'
                            '<span class="nx-dot-ok"></span> Ativo no Chat'
                            '</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        if st.button("Ativar no Chat", key="btn_act_catalog", use_container_width=True):
                            st.session_state.active_model = model_tag_to_install
                            settings.DEFAULT_MODEL = model_tag_to_install
                            st.rerun()
                else:
                    btn_label = f"Baixar e Instalar ({est_size_gb:.1f} GB)"
                    can_dl = compat.get("can_install", True)
                    if st.button(btn_label, key="btn_install_catalog", use_container_width=True, disabled=not can_dl):
                        _execute_download(model_tag_to_install)

    # 4. Parâmetros Específicos por Modelo
    if st.session_state.active_model:
        active_m = st.session_state.active_model
        params = model_manager.get_model_params(active_m)

        st.markdown(
            f'<div class="nx-section-header">'
            f'<div class="nx-section-title">'
            f'{svg("sliders", 16)} Parâmetros de Inferência '
            f'<span class="nx-count-badge" style="color:var(--nx-purple-hi);">{active_m}</span>'
            f'</div>'
            f'<div class="nx-section-sub">Calibração fina da amostragem e limite de contexto do modelo ativo.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            p_col1, p_col2, p_col3 = st.columns(3, gap="large")
            with p_col1:
                new_temp = st.slider(
                    "Temperatura",
                    min_value=0.0,
                    max_value=1.5,
                    value=float(params.get("temperature", 0.7)),
                    step=0.05,
                    help="Valores menores favorecem respostas determinísticas e precisas. Valores maiores estimulam maior diversidade.",
                )
            with p_col2:
                new_tokens = st.slider(
                    "Limite de Tokens (num_predict)",
                    min_value=256,
                    max_value=8192,
                    value=int(params.get("num_predict", 2048)),
                    step=128,
                    help="Quantidade máxima de tokens gerados por resposta.",
                )
            with p_col3:
                new_top_p = st.slider(
                    "Top-P (Nucleus Sampling)",
                    min_value=0.1,
                    max_value=1.0,
                    value=float(params.get("top_p", 0.9)),
                    step=0.05,
                    help="Controla a diversidade cumulativa de amostragem de vocabulário.",
                )

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            col_save, col_reset, _ = st.columns([1.6, 2.0, 3.4], gap="medium")
            with col_save:
                if st.button("Salvar Parâmetros", use_container_width=True):
                    model_manager.save_model_params(
                        active_m,
                        {"temperature": new_temp, "num_predict": new_tokens, "top_p": new_top_p},
                    )
                    st.toast(f"Parâmetros de '{active_m}' salvos com sucesso.")
            with col_reset:
                if st.button("Restaurar Padrões", use_container_width=True):
                    model_manager.reset_model_params(active_m)
                    st.toast(f"Parâmetros de '{active_m}' restaurados.")
                    st.rerun()



def render_about():
    st.markdown(
        '<div class="nx-page"><h2>Sobre</h2><div class="sub">Nexus IA é um assistente autônomo corporativo que opera localmente via Ollama, '
        'com arquitetura multimodelo, memória vetorial de documentos (RAG) e ferramentas seguras de terminal.</div></div>'
        + _kv([
            ("Aplicação", "Nexus IA - Local Corporate Agent"),
            ("Motor de IA", "Ollama (100% Local)"),
            ("Arquitetura de Modelos", "Multimodelo (Llama, Gemma, DeepSeek, Dolphin, Mistral, Qwen, etc.)"),
            ("Formatos Suportados", "PDF, TXT, MD, DOCX"),
            ("Armazenamento Vetorial", "ChromaDB (local)"),
            ("Dados e Privacidade", "100% privados na sua máquina local" if IS_LOCAL else "Servidor remoto"),
        ]),
        unsafe_allow_html=True,
    )


AVATARS = {"assistant": LOGO_IMG}

if page == "Chat":
    # Lê o input do usuário
    prompt = st.chat_input("Como posso ajudar hoje? (Use /shell para executar no terminal)")
    new_user_message = None
    if prompt:
        new_user_message = prompt
        st.session_state.messages.append({"role": "user", "content": prompt})

    # Remove mensagens em branco
    st.session_state.messages = [m for m in st.session_state.messages if m["content"].strip()]

    # Se não há mensagens no histórico, alinha o hero com flexbox centralizado sem cortar o conteúdo
    if not st.session_state.messages:
        st.markdown(
            """<style>
            .block-container {
                padding-top: 1.5rem !important;
                padding-bottom: 2rem !important;
                min-height: calc(100vh - 120px) !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: center !important;
            }
            .nx-welcome-wrap {
                min-height: 0 !important;
                height: auto !important;
                margin: auto 0 !important;
            }
            </style>""",
            unsafe_allow_html=True,
        )
        render_hero()
    else:
        st.markdown('<div class="nx-spacer"></div>', unsafe_allow_html=True)
        # Renderiza todo o histórico prévio
        existing_messages = st.session_state.messages[:-1] if new_user_message else st.session_state.messages
        for message in existing_messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(f'<span class="nx-u"></span>' + message["content"], unsafe_allow_html=True)
            else:
                with st.chat_message("assistant", avatar=AVATARS["assistant"]):
                    formatted_content = format_chat_text(message["content"])
                    st.markdown(f'<span class="nx-a"></span>' + formatted_content, unsafe_allow_html=True)

        # Se há uma nova mensagem de usuário nesta rodada, gera resposta via streaming
        if new_user_message:
            with st.chat_message("user"):
                st.markdown(f'<span class="nx-u"></span>' + new_user_message, unsafe_allow_html=True)

            with st.chat_message("assistant", avatar=AVATARS["assistant"]):
                if not ollama_online:
                    st.error("O Ollama não está ativo. Inicie 'ollama serve' no terminal para gerar respostas.")
                elif not st.session_state.active_model:
                    st.error("Nenhum modelo selecionado ou instalado. Acesse a barra lateral ou a aba 'Modelos' para configurar.")
                elif not model_manager.is_model_installed(st.session_state.active_model):
                    st.warning(
                        f"O modelo '{st.session_state.active_model}' ainda não está baixado no Ollama. "
                        f"Clique no botão 'Baixar e Ativar' na barra lateral para baixá-lo antes de iniciar a conversa."
                    )
                else:
                    message_placeholder = st.empty()
                    message_placeholder.markdown(
                        '<span class="nx-a"></span><div class="nx-typing"><span></span><span></span><span></span></div>',
                        unsafe_allow_html=True,
                    )
                    full_response = ""

                    history_for_llm = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages[:-1]
                        if m["content"].strip()
                    ][-5:]

                    cur_model = st.session_state.active_model
                    cur_options = model_manager.get_model_params(cur_model)

                    try:
                        for chunk in orchestrator.process_message(
                            user_message=new_user_message,
                            history=history_for_llm,
                            persona=selected_persona,
                            use_rag=use_rag,
                            use_tools=use_tools,
                            model=cur_model,
                            options=cur_options,
                        ):
                            full_response += chunk
                            display_text = format_chat_text(full_response)
                            message_placeholder.markdown(f'<span class="nx-a"></span>' + display_text + "▌", unsafe_allow_html=True)

                        if full_response.strip():
                            display_final = format_chat_text(full_response)
                            message_placeholder.markdown(f'<span class="nx-a"></span>' + display_final, unsafe_allow_html=True)
                            st.session_state.messages.append({"role": "assistant", "content": full_response})
                        else:
                            message_placeholder.warning("O modelo não retornou resposta. Tente novamente.")
                    except Exception as e:
                        st.error(f"Erro ao comunicar com o Ollama local. Detalhes: {str(e)}")

elif page == "Configurações":
    render_settings()
elif page == "Arquivos":
    render_files()
elif page == "Modelos":
    render_models()
else:
    render_about()
