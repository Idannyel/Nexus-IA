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
    padding-bottom: 8.5rem !important;
    padding-inline: 1.5rem !important;
    box-sizing: border-box !important;
    position: relative !important;
    z-index: 1 !important;
}

/* Neutraliza margens e paddings espúrios de wrappers internos do Streamlit */
.block-container > [data-testid="stVerticalBlockBorderWrapper"] {
    width: 100% !important;
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}
.block-container [data-testid="stVerticalBlock"] {
    width: 100% !important;
    max-width: 100% !important;
    gap: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}
.block-container .element-container {
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
}
.block-container [data-testid="stMarkdownContainer"] {
    width: 100% !important;
    max-width: 100% !important;
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

/* Cartões da barra lateral */
[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--nx-surface);
    border: 1px solid var(--nx-border);
    border-radius: var(--nx-r-lg);
    padding: 12px 14px;
    box-sizing: border-box;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] { gap: .5rem; }
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
[data-testid="stSidebar"] .stButton > button {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 0 14px;
    background: var(--nx-purple-dk);
    border-color: rgba(117,72,255,.35);
}
.stButton > button p { font-size: var(--nx-fs-sm); margin: 0; }
[data-testid="stSidebar"] .stButton > button::before {
    content: "";
    width: 15px;
    height: 15px;
    background-color: var(--nx-purple-hi);
    -webkit-mask: @icon(trash) center/contain no-repeat;
    mask: @icon(trash) center/contain no-repeat;
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
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 28px 0 0 0;
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
}
.nx-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 14px;
    text-align: left;
    background: var(--nx-surface);
    border: 1px solid var(--nx-border);
    border-radius: var(--nx-r-lg);
    box-shadow: var(--nx-shadow);
    transition: var(--nx-t);
    box-sizing: border-box;
    min-width: 0;
}
.nx-card:hover { transform: translateY(-2px); border-color: var(--nx-border-hi); }
.nx-card .ico {
    width: 38px;
    height: 38px;
    flex: none;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #1B1B45, #141A3A);
    color: var(--nx-purple-hi);
    border: 1px solid var(--nx-border-2);
}
.nx-card .t {
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--nx-text);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.nx-card .d {
    font-size: 0.72rem;
    color: var(--nx-text-2);
    margin-top: 2px;
    line-height: 1.35;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
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

/* ============================ Conversa / Mensagens (Moderna & Minimalista) ============================ */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0.4rem 0 !important;
    margin: 0.25rem 0 !important;
    gap: 12px !important;
    display: flex !important;
    box-sizing: border-box !important;
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    animation: nxfade .35s ease both;
}

/* Balão do usuário: ALINHADO À DIREITA, perfeitamente centralizado com o avatar */
[data-testid="stChatMessage"]:has(img[alt="user avatar"]),
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]),
[data-testid="stChatMessage"]:has(.nx-u) {
    flex-direction: row-reverse !important;
    justify-content: flex-start !important;
    align-items: center !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

[data-testid="stChatMessage"]:has(img[alt="user avatar"]) [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]),
[data-testid="stChatMessage"]:has(.nx-u) [data-testid="stChatMessageContent"] {
    background: rgba(117, 72, 255, 0.16) !important;
    border: 1px solid rgba(117, 72, 255, 0.28) !important;
    border-radius: 16px !important;
    padding: 10px 18px !important;
    width: fit-content !important;
    max-width: 78% !important;
    flex-grow: 0 !important;
    flex-shrink: 1 !important;
    flex-basis: auto !important;
    margin: 0 !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
    box-shadow: 0 2px 10px rgba(0,0,0,.18) !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
}

/* Anula qualquer margem parasita de containers internos do Streamlit dentro do balão */
[data-testid="stChatMessage"]:has(img[alt="user avatar"]) [data-testid="stChatMessageContent"] div,
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) [data-testid="stChatMessageContent"] div,
[data-testid="stChatMessage"]:has(.nx-u) [data-testid="stChatMessageContent"] div {
    margin: 0 !important;
    margin-bottom: 0 !important;
    padding: 0 !important;
    box-sizing: border-box !important;
}

[data-testid="stChatMessage"]:has(img[alt="user avatar"]) [data-testid="stChatMessageContent"] p,
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) [data-testid="stChatMessageContent"] p,
[data-testid="stChatMessage"]:has(.nx-u) [data-testid="stChatMessageContent"] p {
    margin: 0 !important;
    margin-bottom: 0 !important;
    padding: 0 !important;
    line-height: 1.45 !important;
    font-size: 0.95rem !important;
    color: #ffffff !important;
    display: block !important;
}

/* Mensagem do Assistente: ALINHADA À ESQUERDA, sem caixa, sem quadrado, foco puro na leitura fluida */
[data-testid="stChatMessage"]:has(img[alt="assistant avatar"]),
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]),
[data-testid="stChatMessage"]:has(.nx-a) {
    flex-direction: row !important;
    justify-content: flex-start !important;
    align-items: flex-start !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

[data-testid="stChatMessage"]:has(img[alt="assistant avatar"]) [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"]:has(.nx-a) [data-testid="stChatMessageContent"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 3px 0 0 0 !important;
    width: auto !important;
    max-width: 100% !important;
    flex-grow: 1 !important;
    margin: 0 !important;
    text-align: left !important;
}

/* Avatares minimalistas e bem dimensionados */
[data-testid="stChatMessage"] img {
    width: 32px !important;
    height: 32px !important;
    flex-shrink: 0 !important;
    display: block !important;
    margin: 0 !important;
}
[data-testid="stChatMessage"]:has(img[alt="user avatar"]) img {
    border-radius: 50% !important;
    object-fit: cover !important;
}
[data-testid="stChatMessage"]:has(img[alt="assistant avatar"]) img {
    border-radius: 10px !important;
    object-fit: contain !important;
    margin-top: 2px !important;
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

/* ============================ Campo de mensagem (Moderno, Minimalista, Sem Ícones Falsos) ============================ */
[data-testid="stBottom"], [data-testid="stBottom"] > div {
    background: transparent !important;
}
[data-testid="stBottomBlockContainer"] {
    width: 100% !important;
    max-width: var(--nx-chat-w) !important;
    margin-inline: auto !important;
    padding: 0 1.5rem 1.25rem 1.5rem !important;
    box-sizing: border-box !important;
}
[data-testid="stChatInput"] {
    position: relative !important;
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
    max-width: 100% !important;
    padding: 6px 8px 6px 16px !important;
    border-radius: 16px !important;
    background: var(--nx-surface) !important;
    border: 1px solid var(--nx-border-2) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,.35) !important;
    transition: var(--nx-t) !important;
    box-sizing: border-box !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--nx-purple) !important;
    box-shadow: 0 0 0 3px rgba(117,72,255,.18), 0 4px 20px rgba(0,0,0,.35) !important;
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
.nx-files-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100%;
    box-sizing: border-box;
}
.nx-file-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    padding: 0 18px;
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
.nx-file-row:hover {
    border-color: var(--nx-border-hi);
    background: var(--nx-surface-2);
}
.nx-file-left {
    display: flex;
    align-items: center;
    gap: 12px;
    min-width: 0;
    flex: 1 1 auto;
}
.nx-file-ico {
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
.nx-file-name {
    font-size: var(--nx-fs-sm);
    font-weight: 500;
    color: var(--nx-text);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.nx-file-size {
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
    padding: 28px 20px;
    text-align: center;
    border: 1px dashed var(--nx-border-2);
    border-radius: var(--nx-r-lg);
    background: var(--nx-surface);
    box-sizing: border-box;
    width: 100%;
}

/* Botões da aplicação (Excluir, Limpar Chat, etc.) */
div.stButton {
    margin-bottom: 8px !important;
}
div.stButton > button {
    border-radius: var(--nx-r-md) !important;
    background: var(--nx-surface) !important;
    border: 1px solid var(--nx-border) !important;
    color: var(--nx-text-2) !important;
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
}
div.stButton > button:hover {
    background: rgba(255, 75, 75, 0.12) !important;
    border-color: rgba(255, 75, 75, 0.35) !important;
    color: #ff6b6b !important;
}

/* ============================ Responsivo ============================ */
@media (max-width: 1024px) {
    .nx-cards { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 600px) {
    .nx-cards { grid-template-columns: 1fr; }
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
