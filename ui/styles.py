"""Folha de estilos do Nexus IA (tokens + componentes).

Todas as cores, raios e sombras ficam centralizados em variáveis CSS (:root).
Ícones em CSS usam mask-image com SVGs de icons.py (token @icon(nome)).
Interface limpa, profissional e sem poluição decorativa.
"""
import re
from icons import mask_uri

_CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    /* Superfícies */
    --nx-bg:          #080B14;
    --nx-bg-side:     #0A0E19;
    --nx-surface:     #0E1424;
    --nx-surface-2:   #10172A;
    --nx-surface-3:   #151D34;
    /* Bordas */
    --nx-border:      #1B2542;
    --nx-border-2:    #202B48;
    --nx-border-hi:   rgba(117,72,255,.45);
    /* Marca */
    --nx-purple:      #7548FF;
    --nx-purple-hi:   #9B7BFF;
    --nx-purple-dk:   #2B2170;
    --nx-blue:        #315CFF;
    --nx-sky:         #55B7FF;
    --nx-grad:        linear-gradient(135deg, #7548FF 0%, #4F55FF 55%, #315CFF 100%);
    --nx-grad-soft:   linear-gradient(135deg, rgba(117,72,255,.55), rgba(49,92,255,.32));
    /* Texto */
    --nx-text:        #F4F6FF;
    --nx-text-2:      #A9B9D6;
    --nx-text-3:      #6C7BA0;
    /* Estados */
    --nx-ok:          #34D399;
    --nx-err:         #F87171;
    /* Dimensão unificada de conteúdo / conversa */
    --nx-chat-w:      920px;
    --nx-r-sm: 8px;   --nx-r-md: 12px;  --nx-r-lg: 16px;
    --nx-ctl-h: 36px;
    --nx-shadow: 0 8px 24px rgba(0,0,0,.35);
    --nx-t: .18s ease;
    /* Tipografia */
    --nx-fs-xs: .72rem; --nx-fs-sm: .8rem; --nx-fs-md: .92rem; --nx-fs-lg: 1.1rem;
}

html, body {
    overflow-x: hidden !important;
    width: 100% !important;
    max-width: 100vw !important;
    font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif !important;
    background: var(--nx-bg) !important;
    color: var(--nx-text) !important;
}
*, *::before, *::after {
    box-sizing: border-box !important;
}
.nx-ic { display:block; flex:none; }

/* ============================ Estrutura Geral ============================ */
#MainMenu, footer, [data-testid="stDecoration"], [data-testid="stToolbar"] { display:none !important; }
header[data-testid="stHeader"] { background: transparent !important; height: 0 !important; min-height: 0 !important; }
.element-container:has(> [data-testid="stMarkdownContainer"] > style) { display:none !important; }

.stApp {
    background: var(--nx-bg) !important;
    color: var(--nx-text) !important;
    min-height: 100vh !important;
    min-height: 100dvh !important;
    overflow-x: hidden !important;
    width: 100% !important;
}

[data-testid="stMain"], section.main {
    background: transparent !important;
    overflow-x: hidden !important;
    width: 100% !important;
    min-width: 0 !important;
}

/* Container central de conteúdo: largura unificada e centralização perfeita */
.block-container {
    max-width: var(--nx-chat-w) !important;
    width: 100% !important;
    margin-inline: auto !important;
    padding-top: 1.5rem !important;
    padding-bottom: 7.5rem !important;
    padding-inline: 1.5rem !important;
    box-sizing: border-box !important;
    position: relative !important;
    z-index: 1 !important;
}

/* Neutraliza margens desnecessárias do container raiz mantendo respiro natural */
.block-container > [data-testid="stVerticalBlockBorderWrapper"] {
    width: 100% !important;
    max-width: 100% !important;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
}
.block-container [data-testid="stVerticalBlock"] {
    width: 100% !important;
    max-width: 100% !important;
}
.block-container .element-container {
    width: 100% !important;
    max-width: 100% !important;
}
/* Contêineres de seção com borda (st.container(border=True)) com respiro generoso */
.block-container [data-testid="stVerticalBlockBorderWrapper"]:not(:first-child) {
    background: var(--nx-surface) !important;
    border: 1px solid var(--nx-border) !important;
    border-radius: var(--nx-r-lg) !important;
    padding: 24px 28px !important;
    margin-bottom: 36px !important;
    box-sizing: border-box !important;
}
.block-container [data-testid="stMarkdownContainer"] {
    width: 100% !important;
    max-width: 100% !important;
}
/* Anula bordas espúrias de colunas na área principal */
.block-container [data-testid="column"] [data-testid="stVerticalBlockBorderWrapper"],
.block-container [data-testid="column"] [data-testid="stVerticalBlock"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}


::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-thumb { background: var(--nx-surface-3); border-radius: 8px; }
::-webkit-scrollbar-thumb:hover { background: var(--nx-purple-dk); }
:focus-visible { outline: 2px solid var(--nx-purple-hi); outline-offset: 2px; }

/* ============================ Barra superior (Flutuante no topo direito) ============================ */
.nx-top {
    position: fixed;
    top: 12px;
    right: 24px;
    z-index: 50;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 10px;
    pointer-events: none;
}
.nx-top > * { pointer-events: auto; }
.nx-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    height: 30px;
    padding: 0 14px;
    font-size: var(--nx-fs-xs);
    font-weight: 500;
    color: var(--nx-text-2);
    background: var(--nx-surface-2);
    border: 1px solid var(--nx-border-2);
    border-radius: 999px;
    box-sizing: border-box;
    white-space: nowrap;
    box-shadow: 0 2px 8px rgba(0,0,0,.25);
}
.nx-pill .dot { width: 7px; height: 7px; border-radius: 50%; background: var(--nx-ok); box-shadow: 0 0 8px var(--nx-ok); }
.nx-pill.off .dot { background: var(--nx-err); box-shadow: 0 0 8px var(--nx-err); }
.nx-circ {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--nx-surface-2);
    border: 1px solid var(--nx-border-2);
    color: var(--nx-text-2);
    transition: var(--nx-t);
    flex-shrink: 0;
    box-sizing: border-box;
    box-shadow: 0 2px 8px rgba(0,0,0,.25);
    cursor: pointer;
}
.nx-circ svg { display: block; margin: auto; flex-shrink: 0; }
.nx-circ:hover { color: var(--nx-text); border-color: var(--nx-border-hi); }
.nx-spacer { height: 16px; }

/* ============================ Barra lateral ============================ */
[data-testid="stSidebar"] {
    background: var(--nx-bg-side) !important;
    border-right: 1px solid var(--nx-border) !important;
    z-index: 60 !important;
    overflow-x: hidden !important;
}
[data-testid="stSidebarContent"] {
    background: var(--nx-bg-side) !important;
    overflow-x: hidden !important;
}
[data-testid="stSidebarUserContent"] {
    padding: 18px 14px 20px 14px !important;
    overflow-x: hidden !important;
}
[data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] { gap: .6rem !important; }

/* Botão de colapso quando aberta */
[data-testid="stSidebar"] button[kind="header"] {
    width: 32px !important;
    height: 32px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: transparent !important;
    border: none !important;
    color: var(--nx-text-2) !important;
    border-radius: 8px !important;
    transition: var(--nx-t) !important;
    margin: 16px 6px 0 0 !important;
}
[data-testid="stSidebar"] button[kind="header"] > * { display: none !important; }
[data-testid="stSidebar"] button[kind="header"]::after {
    content: "" !important;
    width: 18px !important;
    height: 18px !important;
    background-color: currentColor !important;
    -webkit-mask: @icon(chevrons-left) center/contain no-repeat !important;
    mask: @icon(chevrons-left) center/contain no-repeat !important;
}
[data-testid="stSidebar"] button[kind="header"]:hover {
    color: #fff !important;
    background: var(--nx-surface-3) !important;
}

/* Botão de colapso quando fechada */
[data-testid="collapsedControl"] {
    position: fixed !important;
    top: 12px !important;
    left: 12px !important;
    z-index: 60 !important;
}
[data-testid="collapsedControl"] button {
    width: 34px !important;
    height: 34px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: var(--nx-surface-2) !important;
    border: 1px solid var(--nx-border-2) !important;
    color: var(--nx-text-2) !important;
    border-radius: 10px !important;
    transition: var(--nx-t) !important;
}
[data-testid="collapsedControl"] button > * { display: none !important; }
[data-testid="collapsedControl"] button::after {
    content: "" !important;
    width: 18px !important;
    height: 18px !important;
    background-color: currentColor !important;
    -webkit-mask: @icon(chevrons-left) center/contain no-repeat !important;
    mask: @icon(chevrons-left) center/contain no-repeat !important;
    transform: rotate(180deg) !important;
}
[data-testid="collapsedControl"] button:hover {
    color: #fff !important;
    background: var(--nx-surface-3) !important;
    border-color: var(--nx-border-hi) !important;
}

.nx-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 2px 4px 16px 2px;
    box-sizing: border-box;
}
.nx-brand img {
    width: 44px;
    height: 44px;
    display: block;
    flex-shrink: 0;
    border-radius: 10px;
}
.nx-brand-name {
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: -.01em;
    color: var(--nx-text);
    line-height: 1;
}
.nx-brand-name b { color: var(--nx-purple-hi); font-weight: 700; }

/* Navegação da Sidebar */
[data-testid="stSidebar"] [data-testid="stRadio"] > label { display: none; }
[data-testid="stSidebar"] div[role="radiogroup"] { display: flex; flex-direction: column; gap: 2px; }
[data-testid="stSidebar"] div[role="radiogroup"] > label {
    display: flex;
    align-items: center;
    gap: 12px;
    width: 100%;
    margin: 0;
    padding: 6px 12px;
    min-height: 36px;
    border-radius: var(--nx-r-md);
    cursor: pointer;
    transition: var(--nx-t);
    border: 1px solid transparent;
    box-sizing: border-box;
}
[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child { display: none; }
[data-testid="stSidebar"] div[role="radiogroup"] > label p {
    font-size: var(--nx-fs-md);
    color: var(--nx-text);
    margin: 0;
    font-weight: 500;
}
[data-testid="stSidebar"] div[role="radiogroup"] > label::before {
    content: "";
    width: 18px;
    height: 18px;
    flex: none;
    background-color: var(--nx-sky);
    -webkit-mask-repeat: no-repeat;
    mask-repeat: no-repeat;
    -webkit-mask-position: center;
    mask-position: center;
    -webkit-mask-size: contain;
    mask-size: contain;
}
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-of-type(1)::before { -webkit-mask-image:@icon(chat); mask-image:@icon(chat); }
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-of-type(2)::before { -webkit-mask-image:@icon(settings); mask-image:@icon(settings); }
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-of-type(3)::before { -webkit-mask-image:@icon(file); mask-image:@icon(file); }
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-of-type(4)::before { -webkit-mask-image:@icon(box); mask-image:@icon(box); }
[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-of-type(5)::before { -webkit-mask-image:@icon(info); mask-image:@icon(info); }
[data-testid="stSidebar"] div[role="radiogroup"] > label:hover { background: var(--nx-surface-2); }
[data-testid="stSidebar"] div[role="radiogroup"] > label:focus-within { border-color: var(--nx-purple-hi); }
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(90deg, rgba(117,72,255,.42), rgba(49,92,255,.20));
    border-color: rgba(117,72,255,.30);
}
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked)::before { background-color: #fff; }

/* Cartões da barra lateral (containers diretos com borda) */
[data-testid="stSidebarUserContent"] > [data-testid="stVerticalBlockBorderWrapper"] > [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--nx-surface);
    border: 1px solid var(--nx-border);
    border-radius: var(--nx-r-lg);
    padding: 12px 14px;
    box-sizing: border-box;
}
[data-testid="stSidebarUserContent"] > [data-testid="stVerticalBlockBorderWrapper"] > [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] > [data-testid="stVerticalBlock"] {
    gap: .5rem;
}

/* Reset total de bordas e paddings para colunas e blocos internos da barra lateral */
[data-testid="stSidebar"] [data-testid="column"],
[data-testid="stSidebar"] [data-testid="column"] [data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stSidebar"] [data-testid="column"] [data-testid="stVerticalBlock"],
[data-testid="stSidebar"] [data-testid="column"] .element-container {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    box-shadow: none !important;
}

.nx-ptitle {
    display: flex;
    align-items: center;
    gap: 9px;
    font-size: var(--nx-fs-md);
    font-weight: 600;
    color: var(--nx-text);
    margin: 0;
    padding-bottom: 6px;
}
.nx-ptitle .nx-ic { color: var(--nx-text-2); }
.nx-label { font-size: var(--nx-fs-xs); color: var(--nx-text-2); font-weight: 500; padding: 4px 0 6px 0; }
[data-testid="stSidebar"] label p, [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    font-size: var(--nx-fs-xs);
    color: var(--nx-text-2);
    font-weight: 500;
}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] { margin-bottom: 2px; }
[data-testid="stSidebar"] .stCheckbox label p { font-size: var(--nx-fs-sm); color: var(--nx-text); font-weight: 500; }
[data-testid="stCheckbox"] label { gap: .5rem; }
[data-testid="stCheckbox"] [data-baseweb="checkbox"] > div:first-child { border-radius: 5px; }
[data-testid="stTooltipIcon"] svg { display: none; }
[data-testid="stTooltipIcon"] { width: 15px; height: 15px; display: inline-flex; align-items: center; justify-content: center; }
[data-testid="stTooltipIcon"]::after {
    content: "";
    width: 15px;
    height: 15px;
    background-color: var(--nx-text-2);
    -webkit-mask: @icon(info) center/contain no-repeat;
    mask: @icon(info) center/contain no-repeat;
}

/* Seletores */
[data-baseweb="select"] > div {
    min-height: var(--nx-ctl-h);
    border-radius: var(--nx-r-md);
    background: var(--nx-bg);
    border: 1px solid var(--nx-border-2);
    transition: var(--nx-t);
    font-size: var(--nx-fs-sm);
    box-sizing: border-box;
}
[data-baseweb="select"] > div:hover { border-color: var(--nx-border-hi); }
[data-baseweb="select"] svg { color: var(--nx-text-2); }
[data-baseweb="popover"] ul { background: var(--nx-surface-2); border: 1px solid var(--nx-border-2); border-radius: var(--nx-r-md); }

/* Botões */
.stButton > button, .stDownloadButton > button {
    min-height: var(--nx-ctl-h);
    border-radius: var(--nx-r-md);
    font-weight: 500;
    font-size: var(--nx-fs-sm);
    color: var(--nx-text);
    background: var(--nx-surface-3);
    border: 1px solid var(--nx-border-2);
    transition: var(--nx-t);
    box-sizing: border-box;
}
.stButton > button:hover { border-color: var(--nx-border-hi); color: #fff; background: var(--nx-purple-dk); }
.stButton > button:active { transform: translateY(1px); }
.stButton > button:focus-visible { outline: 2px solid var(--nx-purple-hi); }
.stButton > button:disabled { opacity: .5; cursor: not-allowed; }
/* Contêiner de Ações da Barra Lateral (Limpar Chat / Liberar RAM) - LADO A LADO E SEM BORDA DUPLA */
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 8px !important;
    width: 100% !important;
    max-width: 100% !important;
    margin-top: 10px !important;
    margin-bottom: 2px !important;
    padding: 0 !important;
    box-sizing: border-box !important;
    overflow: visible !important;
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > [data-testid="column"] {
    min-width: 0 !important;
    flex: 1 1 0px !important;
    width: calc(50% - 4px) !important;
    max-width: calc(50% - 4px) !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
    box-sizing: border-box !important;
    overflow: visible !important;
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] div.stButton,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] .stButton {
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
    border: none !important;
    background: transparent !important;
    box-sizing: border-box !important;
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] div.stButton > button,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] .stButton > button {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    width: 100% !important;
    min-height: 34px !important;
    max-height: 34px !important;
    height: 34px !important;
    line-height: 1 !important;
    padding: 0 4px !important;
    margin: 0 !important;
    background: var(--nx-surface-2) !important;
    border: 1px solid var(--nx-border) !important;
    border-radius: var(--nx-r-sm) !important;
    color: var(--nx-text-2) !important;
    font-size: 0.76rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.01em !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    box-sizing: border-box !important;
    box-shadow: none !important;
    outline: none !important;
    position: static !important;
    transform: none !important;
    transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease, box-shadow 0.15s ease !important;
    cursor: pointer !important;
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] div.stButton > button:hover,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] .stButton > button:hover {
    background: var(--nx-surface-3) !important;
    border-color: var(--nx-border-hi) !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(117, 72, 255, 0.18) !important;
    transform: none !important;
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] div.stButton > button:active,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] .stButton > button:active {
    background: var(--nx-surface-2) !important;
    transform: translateY(1px) !important;
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] div.stButton > button:focus,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] .stButton > button:focus {
    border-color: var(--nx-border-hi) !important;
    outline: none !important;
    transform: none !important;
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] div.stButton > button p,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] .stButton > button p {
    font-size: 0.76rem !important;
    font-weight: 500 !important;
    margin: 0 !important;
    padding: 0 !important;
    text-align: center !important;
    line-height: 1 !important;
    width: 100% !important;
    color: inherit !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    display: block !important;
}


/* Upload */
[data-testid="stFileUploader"] section { padding: 0; }
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 14px 12px;
    background: var(--nx-bg);
    border: 1px dashed var(--nx-border-hi);
    border-radius: var(--nx-r-md);
    transition: var(--nx-t);
    box-sizing: border-box;
    width: 100%;
}
[data-testid="stFileUploaderDropzone"]:hover { background: rgba(117,72,255,.07); border-color: var(--nx-purple-hi); }
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] {
    display: flex;
    flex-direction: column;
    align-items: center;
    align-self: stretch;
    gap: 8px;
    margin: 0;
    width: 100%;
    text-align: center;
    box-sizing: border-box;
}
[data-testid="stFileUploaderDropzoneInstructions"] > * { display: none; }
[data-testid="stFileUploaderDropzoneInstructions"]::before {
    content: "";
    width: 32px;
    height: 32px;
    background-color: var(--nx-purple-hi);
    -webkit-mask: @icon(cloud-up) center/contain no-repeat;
    mask: @icon(cloud-up) center/contain no-repeat;
}
[data-testid="stFileUploaderDropzoneInstructions"]::after {
    content: "Arraste e solte arquivos aqui\A Limite: 200MB por arquivo\A (PDF, TXT, MD, DOCX)";
    white-space: pre-line;
    text-align: center;
    font-size: var(--nx-fs-xs);
    line-height: 1.55;
    color: var(--nx-text-2);
}
[data-testid="stFileUploaderDropzone"] button {
    font-size: 0;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    min-height: 32px;
    padding: 0 16px;
    border: none;
    border-radius: 10px;
    background: var(--nx-grad);
    color: #fff;
    box-sizing: border-box;
}
[data-testid="stFileUploaderDropzone"] button::before {
    content: "";
    width: 15px;
    height: 15px;
    background-color: #fff;
    -webkit-mask: @icon(folder) center/contain no-repeat;
    mask: @icon(folder) center/contain no-repeat;
}
[data-testid="stFileUploaderDropzone"] button::after { content: "Procurar arquivos"; font-size: var(--nx-fs-sm); font-weight: 500; }
[data-testid="stFileUploaderDropzone"] button:hover { filter: brightness(1.12); }
[data-testid="stFileUploaderFile"] { color: var(--nx-text-2); }
[data-testid="stAlert"] { border-radius: var(--nx-r-md); border: 1px solid var(--nx-border-2); background: var(--nx-surface-2); }

/* ============================ Cabeçalho central ============================ */
@keyframes nxfade { from {opacity: 0; transform: translateY(6px);} to {opacity: 1; transform: none;} }
.nx-welcome-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: calc(100vh - 220px);
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
    margin: 0 auto;
    animation: nxfade .45s ease both;
}
.nx-hero {
    text-align: center;
    padding: 0;
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
}
.nx-hero img {
    width: 68px;
    height: 68px;
    display: inline-block;
    border-radius: 16px;
}
.nx-hero h1 {
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: -.02em;
    margin: 12px 0 6px 0;
    padding: 0;
    color: var(--nx-text);
    line-height: 1.15;
}
.nx-hero h1 b, .nx-greet b {
    background: linear-gradient(90deg, #9B7BFF, #7548FF);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-weight: 700;
}
.nx-hero p {
    color: var(--nx-text-2);
    font-size: var(--nx-fs-sm);
    margin: 0;
}

.nx-cards {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
    margin: 28px 0 0 0;
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
}
.nx-card {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 18px;
    text-align: left;
    background: var(--nx-surface);
    border: 1px solid var(--nx-border);
    border-radius: var(--nx-r-lg);
    box-shadow: var(--nx-shadow);
    transition: var(--nx-t);
    box-sizing: border-box;
    min-width: 0;
    min-height: 74px;
}
.nx-card:hover {
    transform: translateY(-2px);
    border-color: var(--nx-border-hi);
    background: var(--nx-surface-2);
}
.nx-card .ico {
    width: 42px;
    height: 42px;
    flex: none;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(117,72,255,.15), rgba(49,92,255,.15));
    color: var(--nx-purple-hi);
    border: 1px solid var(--nx-border-2);
}
.nx-card .cnt {
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-width: 0;
    flex: 1 1 auto;
    overflow: hidden;
}
.nx-card .t {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--nx-text);
    margin-bottom: 3px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.25;
}
.nx-card .d {
    font-size: 0.77rem;
    color: var(--nx-text-2);
    margin: 0;
    line-height: 1.4;
    white-space: normal;
    word-break: normal;
    overflow-wrap: break-word;
}

.nx-greet-wrap {
    text-align: center;
    margin-top: 36px;
    width: 100%;
    box-sizing: border-box;
    animation: nxfade .6s ease both;
}
.nx-greet { font-size: 1.6rem; font-weight: 700; color: var(--nx-text); letter-spacing: -.01em; }
.nx-greet-sub {
    max-width: 520px;
    margin: 10px auto 0 auto;
    font-size: var(--nx-fs-sm);
    line-height: 1.6;
    color: var(--nx-text-2);
    text-wrap: balance;
}

/* ============================ Conversa / Mensagens (ChatGPT & Gemini Style) ============================ */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 1.25rem 0 !important;
    display: flex !important;
    box-sizing: border-box !important;
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    animation: nxfade .25s ease both;
}

/* ================== Mensagem do Usuário (Estilo ChatGPT / Gemini) ================== */
/* Alinhado à direita, balão único e elegante, sem moldura externa */
[data-testid="stChatMessage"]:has(img[alt="user"]),
[data-testid="stChatMessage"]:has(img[alt="user avatar"]),
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarCustom"]),
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]),
[data-testid="stChatMessage"]:has(.nx-u) {
    flex-direction: row !important;
    justify-content: flex-end !important;
    align-items: flex-end !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    margin-left: auto !important;
    gap: 0 !important;
}

/* Oculta completamente o avatar do usuário (como no ChatGPT e Gemini para manter o visual limpo e minimalista) */
[data-testid="stChatMessage"]:has(img[alt="user"]) > :not([data-testid="stChatMessageContent"]),
[data-testid="stChatMessage"]:has(img[alt="user avatar"]) > :not([data-testid="stChatMessageContent"]),
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) > :not([data-testid="stChatMessageContent"]),
[data-testid="stChatMessage"]:has([aria-label*="user" i]) > :not([data-testid="stChatMessageContent"]),
[data-testid="stChatMessage"]:has(.nx-u) > :not([data-testid="stChatMessageContent"]),
[data-testid="stChatMessage"]:has(.nx-u) > :first-child:not([data-testid="stChatMessageContent"]),
[data-testid="stChatMessage"]:has([aria-label*="user" i]) > :first-child:not([data-testid="stChatMessageContent"]) {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    min-width: 0 !important;
    max-width: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    background: transparent !important;
    visibility: hidden !important;
    pointer-events: none !important;
    opacity: 0 !important;
}

/* Balão de fala do usuário */
[data-testid="stChatMessage"]:has(img[alt="user"]) [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"]:has(img[alt="user avatar"]) [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarCustom"]) [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"]:has(.nx-u) [data-testid="stChatMessageContent"] {
    background: #1e2232 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 20px !important;
    padding: 10px 18px !important;
    width: fit-content !important;
    max-width: 72% !important;
    flex-grow: 0 !important;
    flex-shrink: 1 !important;
    flex-basis: auto !important;
    margin: 0 !important;
    margin-left: auto !important;
    margin-right: 0 !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25) !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
}

[data-testid="stChatMessage"]:has(img[alt="user"]) [data-testid="stChatMessageContent"] div,
[data-testid="stChatMessage"]:has(img[alt="user avatar"]) [data-testid="stChatMessageContent"] div,
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) [data-testid="stChatMessageContent"] div,
[data-testid="stChatMessage"]:has(.nx-u) [data-testid="stChatMessageContent"] div {
    margin: 0 !important;
    margin-bottom: 0 !important;
    padding: 0 !important;
    box-sizing: border-box !important;
}

[data-testid="stChatMessage"]:has(img[alt="user"]) [data-testid="stChatMessageContent"] p,
[data-testid="stChatMessage"]:has(img[alt="user avatar"]) [data-testid="stChatMessageContent"] p,
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) [data-testid="stChatMessageContent"] p,
[data-testid="stChatMessage"]:has(.nx-u) [data-testid="stChatMessageContent"] p {
    margin: 0 !important;
    margin-bottom: 0 !important;
    padding: 0 !important;
    line-height: 1.5 !important;
    font-size: 0.95rem !important;
    color: #f1f5f9 !important;
    display: block !important;
    font-weight: 400 !important;
}

/* ================== Mensagem da IA / Assistente (Estilo ChatGPT / Gemini) ================== */
/* Alinhada à esquerda, leitura fluida, sem balão, sem moldura */
[data-testid="stChatMessage"]:has(img[alt="assistant"]),
[data-testid="stChatMessage"]:has(img[alt="assistant avatar"]),
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]),
[data-testid="stChatMessage"]:has(.nx-a) {
    flex-direction: row !important;
    justify-content: flex-start !important;
    align-items: flex-start !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    gap: 14px !important;
    margin: 1.5rem 0 !important;
}

/* Ícone da IA elegante */
[data-testid="stChatMessage"]:has(img[alt="assistant"]) [data-testid="stChatMessageAvatarContainer"],
[data-testid="stChatMessage"]:has(img[alt="assistant avatar"]) [data-testid="stChatMessageAvatarContainer"] {
    margin-top: 2px !important;
    flex-shrink: 0 !important;
}
[data-testid="stChatMessage"]:has(img[alt="assistant"]) img,
[data-testid="stChatMessage"]:has(img[alt="assistant avatar"]) img {
    width: 28px !important;
    height: 28px !important;
    border-radius: 8px !important;
    object-fit: contain !important;
    display: block !important;
    margin: 0 !important;
    box-shadow: 0 2px 8px rgba(117, 72, 255, 0.3) !important;
}

/* Conteúdo da resposta da IA */
[data-testid="stChatMessage"]:has(img[alt="assistant"]) [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"]:has(img[alt="assistant avatar"]) [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"]:has(.nx-a) [data-testid="stChatMessageContent"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    width: auto !important;
    max-width: 100% !important;
    flex: 1 1 auto !important;
    margin: 0 !important;
    text-align: left !important;
    color: #e2e8f0 !important;
}

[data-testid="stChatMessage"]:has(img[alt="assistant"]) [data-testid="stChatMessageContent"] p,
[data-testid="stChatMessage"]:has(img[alt="assistant avatar"]) [data-testid="stChatMessageContent"] p,
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) [data-testid="stChatMessageContent"] p {
    font-size: 1rem !important;
    line-height: 1.75 !important;
    color: #e2e8f0 !important;
    margin-bottom: 0.85rem !important;
}

/* Conteúdo de mensagem */
[data-testid="stChatMessageContent"] {
    min-width: 0 !important;
    max-width: 100% !important;
    overflow-wrap: anywhere !important;
    word-break: break-word !important;
    box-sizing: border-box !important;
}
[data-testid="stChatMessageContent"] > * {
    min-width: 0 !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
}
[data-testid="stChatMessageContent"] p,
[data-testid="stChatMessageContent"] li {
    font-size: .96rem !important;
    line-height: 1.7 !important;
    color: var(--nx-text) !important;
    margin-bottom: .5rem !important;
}
[data-testid="stChatMessageContent"] p:last-child {
    margin-bottom: 0 !important;
}
[data-testid="stChatMessageContent"] pre {
    background: var(--nx-surface-2) !important;
    border: 1px solid var(--nx-border) !important;
    border-radius: var(--nx-r-md) !important;
    padding: 14px 16px !important;
    max-width: 100% !important;
    overflow-x: auto !important;
    box-sizing: border-box !important;
    margin: 10px 0 !important;
}
[data-testid="stChatMessageContent"] code {
    font-family: 'Consolas', 'Fira Code', monospace !important;
    font-size: .88rem !important;
    color: var(--nx-sky) !important;
}
[data-testid="stChatMessageContent"] table {
    width: 100% !important;
    max-width: 100% !important;
    border-collapse: collapse !important;
    margin: 10px 0 !important;
    display: block !important;
    overflow-x: auto !important;
    box-sizing: border-box !important;
}
[data-testid="stChatMessageContent"] th,
[data-testid="stChatMessageContent"] td {
    border: 1px solid var(--nx-border-2) !important;
    padding: 8px 12px !important;
    font-size: var(--nx-fs-sm) !important;
    box-sizing: border-box !important;
}
[data-testid="stChatMessageContent"] th {
    background: var(--nx-surface-2) !important;
    color: var(--nx-text) !important;
}
[data-testid="stChatMessageContent"] td {
    background: var(--nx-surface) !important;
    color: var(--nx-text-2) !important;
}
[data-testid="stChatMessageContent"] img {
    max-width: 100% !important;
    height: auto !important;
    border-radius: var(--nx-r-md) !important;
    box-sizing: border-box !important;
}
.nx-u, .nx-a { display: none; }
.nx-typing { display: inline-flex; gap: 6px; padding: 6px 0; align-items: center; }
.nx-typing span { width: 6px; height: 6px; border-radius: 50%; background: var(--nx-purple-hi); animation: nxblink 1.2s infinite ease-in-out; }
.nx-typing span:nth-child(2){animation-delay:.2s} .nx-typing span:nth-child(3){animation-delay:.4s}
@keyframes nxblink { 0%,80%,100%{opacity:.25; transform:scale(.8);} 40%{opacity:1; transform:scale(1);} }

/* ============================ Campo de mensagem / Shield inferior (Estilo ChatGPT / Gemini) ============================ */
/* Fundo protetor em degradê suave: dissolve o texto antes de chegar à barra e impede sobreposição */
[data-testid="stBottom"] {
    position: sticky !important;
    bottom: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
    z-index: 40 !important;
    background: linear-gradient(180deg, rgba(8, 11, 20, 0) 0%, rgba(8, 11, 20, 0.75) 25%, #080B14 55%, #080B14 100%) !important;
    padding-top: 36px !important;
    box-sizing: border-box !important;
}
[data-testid="stBottom"] > div {
    width: 100% !important;
    max-width: 100% !important;
    background: transparent !important;
    box-sizing: border-box !important;
}
[data-testid="stBottomBlockContainer"] {
    width: 100% !important;
    max-width: var(--nx-chat-w) !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding: 0 1.5rem 1.4rem 1.5rem !important;
    box-sizing: border-box !important;
}
[data-testid="stBottomBlockContainer"] [data-testid="stVerticalBlock"],
[data-testid="stBottomBlockContainer"] .element-container {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
}
[data-testid="stChatInput"] {
    position: relative !important;
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    padding: 10px 14px 10px 22px !important;
    border-radius: 22px !important;
    background: #0E1424 !important;
    border: 1px solid var(--nx-border-2) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,.60) !important;
    transition: var(--nx-t) !important;
    box-sizing: border-box !important;
    z-index: 50 !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--nx-purple) !important;
    box-shadow: 0 0 0 3px rgba(117,72,255,.22), 0 8px 32px rgba(0,0,0,.60) !important;
}
/* Remove completamente ícones falsos decorativos (paperclip e sliders) */
[data-testid="stChatInput"]::before,
[data-testid="stChatInput"]::after,
[data-testid="stChatInput"] > div::before,
[data-testid="stChatInput"] > div::after {
    display: none !important;
    content: none !important;
}
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] [data-baseweb="textarea"],
[data-testid="stChatInput"] [data-baseweb="base-input"] {
    flex: 1 1 auto !important;
    min-width: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    position: relative !important;
    box-sizing: border-box !important;
}
[data-testid="stChatInput"] textarea {
    color: var(--nx-text) !important;
    font-size: var(--nx-fs-sm) !important;
    padding: 8px 12px 8px 0 !important;
    min-width: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    box-sizing: border-box !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--nx-text-3) !important;
    opacity: 1 !important;
}
[data-testid="stChatInput"] button {
    width: 36px !important;
    height: 36px !important;
    border-radius: 10px !important;
    background: var(--nx-grad) !important;
    color: #fff !important;
    border: none !important;
    transition: var(--nx-t) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
    flex-shrink: 0 !important;
    cursor: pointer !important;
    padding: 0 !important;
    margin: 0 !important;
    box-shadow: 0 2px 8px rgba(117, 72, 255, 0.3) !important;
}
[data-testid="stChatInput"] button svg {
    display: block !important;
    width: 18px !important;
    height: 18px !important;
    fill: #ffffff !important;
    color: #ffffff !important;
    margin: auto !important;
}
[data-testid="stChatInput"] button svg path {
    fill: #ffffff !important;
}
[data-testid="stChatInput"] button::after {
    display: none !important;
    content: none !important;
}
[data-testid="stChatInput"] button:hover:not(:disabled) {
    filter: brightness(1.15) !important;
    transform: scale(1.04) !important;
}
[data-testid="stChatInput"] button:disabled {
    opacity: .45 !important;
    filter: grayscale(0.3) !important;
    cursor: not-allowed !important;
    box-shadow: none !important;
}

/* ============================ Páginas (Configurações, Arquivos, etc.) ============================ */
.nx-page {
    padding-top: 18px;
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
}
.nx-page h2 {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 0 6px 0;
    color: var(--nx-text);
    letter-spacing: -.01em;
}
.nx-page .sub {
    color: var(--nx-text-2);
    font-size: var(--nx-fs-sm);
    margin-bottom: 22px;
    line-height: 1.5;
}
.nx-kv {
    display: grid;
    grid-template-columns: 240px 1fr;
    gap: 1px;
    background: var(--nx-border);
    border: 1px solid var(--nx-border);
    border-radius: var(--nx-r-lg);
    overflow: hidden;
    margin-bottom: 20px;
    box-sizing: border-box;
    width: 100%;
}
.nx-kv div {
    background: var(--nx-surface);
    padding: 12px 18px;
    font-size: var(--nx-fs-sm);
    color: var(--nx-text);
    box-sizing: border-box;
    word-break: break-word;
}
.nx-kv div.k {
    color: var(--nx-text-2);
    font-weight: 500;
    background: var(--nx-surface-2);
}
.nx-files-header-meta {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: var(--nx-fs-sm);
    color: var(--nx-text-2);
    min-height: 44px;
    height: 44px;
    box-sizing: border-box;
}
.nx-dot-ok {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--nx-ok);
    box-shadow: 0 0 8px var(--nx-ok);
    flex-shrink: 0;
}
.nx-files-divider {
    height: 6px;
}
.nx-files-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100%;
    box-sizing: border-box;
}
.nx-file-row,
.nx-file-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    padding: 0 16px;
    min-height: 44px;
    height: 44px;
    background: var(--nx-surface);
    border: 1px solid var(--nx-border);
    border-radius: var(--nx-r-md);
    box-sizing: border-box;
    transition: var(--nx-t);
    width: 100%;
    margin-bottom: 8px;
}
.nx-file-row:hover,
.nx-file-card:hover {
    border-color: var(--nx-border-hi);
    background: var(--nx-surface-2);
}
.nx-file-left,
.nx-file-card-left {
    display: flex;
    align-items: center;
    gap: 12px;
    min-width: 0;
    flex: 1 1 auto;
}
.nx-file-card-text {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    min-width: 0;
    flex: 1 1 auto;
}
.nx-file-ico,
.nx-file-card-ico {
    width: 28px;
    height: 28px;
    border-radius: 8px;
    background: var(--nx-surface-3);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--nx-sky);
    flex-shrink: 0;
}
.nx-file-name,
.nx-file-card-name {
    font-size: var(--nx-fs-sm);
    font-weight: 500;
    color: var(--nx-text);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.nx-file-size,
.nx-file-card-size {
    font-size: var(--nx-fs-xs);
    color: var(--nx-text-2);
    background: var(--nx-surface-3);
    padding: 3px 8px;
    border-radius: 999px;
    border: 1px solid var(--nx-border-2);
    flex-shrink: 0;
}
.nx-empty {
    color: var(--nx-text-3);
    font-size: var(--nx-fs-sm);
    padding: 36px 24px;
    text-align: center;
    border: 1px dashed var(--nx-border-2);
    border-radius: var(--nx-r-lg);
    background: var(--nx-surface);
    box-sizing: border-box;
    width: 100%;
    margin: 12px 0;
}
.nx-empty-ico {
    color: var(--nx-purple-hi);
    margin-bottom: 12px;
    display: flex;
    justify-content: center;
}
.nx-empty-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--nx-text);
    margin-bottom: 6px;
}
.nx-empty-desc {
    font-size: var(--nx-fs-sm);
    color: var(--nx-text-2);
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.5;
}

/* Botões da aplicação (Geral, Ativar, Salvar, etc.) */
div.stButton {
    margin: 0 !important;
    margin-bottom: 8px !important;
    width: 100% !important;
}
div.stButton > button {
    border-radius: var(--nx-r-md) !important;
    background: var(--nx-surface) !important;
    border: 1px solid var(--nx-border) !important;
    color: var(--nx-text) !important;
    font-size: var(--nx-fs-sm) !important;
    font-weight: 500 !important;
    min-height: 40px !important;
    height: 40px !important;
    padding: 0 16px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: nowrap !important;
    word-break: keep-all !important;
    transition: var(--nx-t) !important;
    box-sizing: border-box !important;
    margin: 0 !important;
    width: 100% !important;
}
div.stButton > button:hover {
    background: var(--nx-surface-3) !important;
    border-color: var(--nx-border-hi) !important;
    color: #ffffff !important;
    box-shadow: 0 2px 10px rgba(117, 72, 255, 0.2) !important;
}
div.stButton > button:active {
    transform: scale(0.99) !important;
}

/* ============================ Hub de Modelos & Hardware ============================ */
.nx-page {
    margin-bottom: 30px;
}
.nx-page h2 {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--nx-text);
    margin: 0 0 8px 0;
    letter-spacing: -0.02em;
}
.nx-page .sub {
    font-size: 0.86rem;
    color: var(--nx-text-2);
    line-height: 1.5;
}

/* Cabeçalhos de Seção com Hierarquia Clara */
.nx-section-header {
    margin-top: 36px;
    margin-bottom: 16px;
}
.nx-section-header.first {
    margin-top: 8px;
}
.nx-section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--nx-text);
    display: flex;
    align-items: center;
    gap: 8px;
    letter-spacing: -0.01em;
}
.nx-section-sub {
    font-size: 0.82rem;
    color: var(--nx-text-3);
    margin-top: 4px;
    line-height: 1.45;
}

.nx-hw-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin: 14px 0 40px 0;
    width: 100%;
    box-sizing: border-box;
}
.nx-hw-card {
    background: var(--nx-surface-2);
    border: 1px solid var(--nx-border);
    border-radius: var(--nx-r-md);
    padding: 16px 18px;
    box-sizing: border-box;
    transition: var(--nx-t);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 110px;
}
.nx-hw-card:hover {
    border-color: var(--nx-border-hi);
    background: var(--nx-surface-3);
}
.nx-hw-title {
    display: flex;
    align-items: center;
    gap: 6px;
    color: var(--nx-text-3);
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}
.nx-hw-val {
    font-size: 1.22rem;
    font-weight: 700;
    color: #ffffff;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.2;
}
.nx-hw-val .unit {
    font-size: 0.74rem;
    font-weight: 400;
    color: var(--nx-text-3);
    margin-left: 4px;
}
.nx-hw-sub {
    font-size: 0.75rem;
    color: var(--nx-text-2);
    margin-top: 8px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    display: flex;
    align-items: center;
    gap: 6px;
}

.nx-count-badge {
    display: inline-flex;
    align-items: center;
    font-size: var(--nx-fs-xs);
    font-weight: 500;
    color: var(--nx-text-3);
    background: var(--nx-surface-3);
    border: 1px solid var(--nx-border-2);
    padding: 2px 8px;
    border-radius: 999px;
    margin-left: 8px;
}

.nx-dot-ok {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--nx-ok);
    box-shadow: 0 0 6px var(--nx-ok);
    flex-shrink: 0;
}
.nx-dot-err {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--nx-err);
    box-shadow: 0 0 6px var(--nx-err);
    flex-shrink: 0;
}

/* Lista de modelos instalados com respiro e alinhamento */
.nx-model-table-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    padding: 0 18px;
    min-height: 48px;
    height: 48px;
    background: var(--nx-surface-2);
    border: 1px solid var(--nx-border);
    border-radius: var(--nx-r-md);
    box-sizing: border-box;
    transition: var(--nx-t);
    width: 100%;
    margin-bottom: 10px;
}
.nx-model-table-card:hover {
    border-color: var(--nx-border-hi);
    background: var(--nx-surface-3);
}
.nx-model-table-card.active {
    border-color: var(--nx-purple);
    background: rgba(117, 72, 255, 0.08);
    box-shadow: 0 0 12px rgba(117, 72, 255, 0.12);
}
.nx-model-table-left {
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 0;
    flex: 1 1 auto;
}
.nx-model-table-ico {
    width: 28px;
    height: 28px;
    border-radius: 8px;
    background: var(--nx-surface-3);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--nx-sky);
    flex-shrink: 0;
}
.nx-model-table-card.active .nx-model-table-ico {
    color: var(--nx-purple-hi);
    background: rgba(117, 72, 255, 0.2);
}
.nx-model-table-meta {
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 0;
    flex: 1 1 auto;
}
.nx-model-table-name {
    font-size: var(--nx-fs-sm);
    font-weight: 600;
    color: var(--nx-text);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.nx-model-table-tags {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-left: auto;
    flex-shrink: 0;
}
.nx-tag-chip {
    font-size: var(--nx-fs-xs);
    color: var(--nx-text-2);
    background: var(--nx-surface-3);
    padding: 2px 8px;
    border-radius: 6px;
    border: 1px solid var(--nx-border-2);
    white-space: nowrap;
    display: inline-flex;
    align-items: center;
}
.nx-tag-chip.accent {
    color: var(--nx-purple-hi);
    background: rgba(117, 72, 255, 0.14);
    border-color: rgba(117, 72, 255, 0.35);
    font-weight: 600;
}

/* Painel de Instalação e Especificações */
.nx-install-card-wrap {
    background: var(--nx-surface);
    border: 1px solid var(--nx-border);
    border-radius: var(--nx-r-lg);
    padding: 18px 20px 20px 20px;
    box-sizing: border-box;
    margin-bottom: 24px;
    width: 100%;
}
.nx-spec-badge-bar {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    background: var(--nx-surface-2);
    border: 1px solid var(--nx-border-2);
    border-radius: var(--nx-r-md);
    margin: 12px 0 16px 0;
    flex-wrap: wrap;
    box-sizing: border-box;
}
.nx-spec-badge-item {
    font-size: var(--nx-fs-xs);
    color: var(--nx-text-2);
    display: inline-flex;
    align-items: center;
    gap: 4px;
}
.nx-spec-badge-item strong {
    color: var(--nx-text);
}
.nx-spec-badge-item code {
    background: rgba(117, 72, 255, 0.12);
    color: var(--nx-purple-hi);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: var(--nx-fs-xs);
    border: 1px solid rgba(117, 72, 255, 0.25);
}
.nx-spec-desc-text {
    font-size: var(--nx-fs-xs);
    color: var(--nx-text-3);
    line-height: 1.45;
    width: 100%;
    margin-top: 4px;
    border-top: 1px solid var(--nx-border);
    padding-top: 6px;
}

.nx-already-active-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    height: 40px;
    min-height: 40px;
    border-radius: var(--nx-r-md);
    background: rgba(52, 211, 153, 0.08);
    border: 1px solid rgba(52, 211, 153, 0.25);
    color: var(--nx-ok);
    font-size: var(--nx-fs-xs);
    font-weight: 600;
    width: 100%;
    box-sizing: border-box;
}

.nx-model-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-bottom: 20px;
    width: 100%;
    box-sizing: border-box;
}
.nx-model-card {
    background: var(--nx-surface);
    border: 1px solid var(--nx-border);
    border-radius: var(--nx-r-lg);
    padding: 16px 18px;
    box-sizing: border-box;
    transition: var(--nx-t);
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.nx-model-card:hover { border-color: var(--nx-border-hi); }
.nx-model-card.active {
    border-color: var(--nx-purple);
    box-shadow: 0 0 18px rgba(117, 72, 255, 0.15);
}
.nx-model-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
}
.nx-model-card-title {
    font-size: 1.02rem;
    font-weight: 600;
    color: var(--nx-text);
}
.nx-model-card-desc {
    font-size: var(--nx-fs-sm);
    color: var(--nx-text-2);
    line-height: 1.45;
}

.nx-sidebar-model-badge {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 12px;
    background: var(--nx-surface-2);
    border: 1px solid var(--nx-border-2);
    border-radius: var(--nx-r-md);
    margin-top: 4px;
    margin-bottom: 10px;
    width: 100%;
    box-sizing: border-box;
}
.nx-badge-tag {
    display: inline-flex;
    align-items: center;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: var(--nx-fs-xs);
    font-weight: 600;
    background: rgba(117, 72, 255, 0.15);
    color: var(--nx-purple-hi);
    border: 1px solid rgba(117, 72, 255, 0.3);
}
.nx-badge-name {
    font-size: var(--nx-fs-xs);
    color: var(--nx-text-2);
    font-weight: 500;
}

/* Blocos de Raciocínio Analítico (<think>) */
.nx-think-details {
    background: rgba(14, 20, 36, 0.65);
    border: 1px solid var(--nx-border);
    border-left: 3px solid var(--nx-purple);
    border-radius: var(--nx-r-sm);
    margin: 12px 0;
    padding: 8px 12px;
    font-size: var(--nx-fs-sm);
    color: var(--nx-text-2);
    transition: var(--nx-t);
}
.nx-think-details[open] {
    background: rgba(16, 23, 42, 0.85);
    border-color: var(--nx-border-2);
}
.nx-think-title {
    cursor: pointer;
    font-size: var(--nx-fs-xs);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--nx-purple-hi);
    display: flex;
    align-items: center;
    gap: 6px;
    user-select: none;
    outline: none;
}
.nx-think-title:hover {
    color: var(--nx-text);
}
.nx-think-body {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px dashed var(--nx-border);
    line-height: 1.6;
    color: var(--nx-text-2);
    font-size: 0.86rem;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ============================ Responsivo ============================ */
@media (max-width: 1024px) {
    .nx-cards { grid-template-columns: repeat(2, 1fr); }
    .nx-hw-grid { grid-template-columns: repeat(2, 1fr); }
    .nx-model-showcase { grid-template-columns: 1fr; }
}
@media (max-width: 600px) {
    .nx-cards { grid-template-columns: 1fr; }
    .nx-hw-grid { grid-template-columns: 1fr; }
    .nx-model-showcase { grid-template-columns: 1fr; }
    .nx-model-table-tags { display: none !important; }
    .nx-spec-badge-bar { flex-direction: column; align-items: flex-start; gap: 6px; }
    .nx-top { top: 8px; right: 12px; gap: 6px; }
    .nx-hero h1 { font-size: 1.7rem; }
    .nx-greet { font-size: 1.3rem; }
    .block-container { padding-inline: 1rem !important; }
    [data-testid="stBottomBlockContainer"] { padding-inline: 1rem !important; }
    .nx-kv { grid-template-columns: 1fr; }
}
</style>
"""


def build_css() -> str:
    return re.sub(r"@icon\(([\w-]+)\)", lambda m: mask_uri(m.group(1)), _CSS)
