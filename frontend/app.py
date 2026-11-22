from pathlib import Path
import sys

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag_engine import tanya_rag


st.set_page_config(
    page_title="Ruang Tanya · Asisten Dokumen",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root { --ink:#19233b; --muted:#71809b; --violet:#6b5ce7; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
    .stApp { background:#f7f8fc; color:var(--ink); }
    [data-testid="stHeader"] { background:rgba(247,248,252,.86); }
    [data-testid="stSidebar"] { background:#fff; border-right:1px solid #edf0f6; }
    [data-testid="stSidebar"] > div:first-child { padding-top:1.5rem; }
    .block-container { max-width:1120px; padding-top:2.2rem; padding-bottom:7rem; }
    .brand { display:flex; align-items:center; gap:12px; padding:6px 4px 28px; }
    .brand-mark { width:42px; height:42px; display:grid; place-items:center; color:white; border-radius:14px; font-size:21px; background:linear-gradient(135deg,#7868f3,#5545d3); box-shadow:0 8px 20px #6758db38; }
    .brand-name { font:800 17px 'Manrope',sans-serif; color:#1d2741; letter-spacing:-.5px; }
    .brand-sub { color:#8a95aa; font-size:11px; margin-top:1px; }
    .side-label { color:#a1aabd; font-size:10px; font-weight:700; letter-spacing:1.4px; text-transform:uppercase; margin:8px 0 9px; }
    .status-card { background:#f7f8fc; border:1px solid #edf0f6; border-radius:14px; padding:12px 13px; margin:10px 0 20px; }
    .status-row { display:flex; align-items:center; gap:8px; color:#46516a; font-size:12px; font-weight:600; }
    .status-dot { width:8px; height:8px; border-radius:50%; background:#37bd8b; box-shadow:0 0 0 4px #37bd8b1b; }
    .status-note { color:#8994a9; font-size:11px; line-height:1.5; margin:8px 0 0 16px; }
    .main-eyebrow { display:inline-flex; align-items:center; gap:7px; padding:6px 11px; border-radius:99px; color:#6557d9; background:#eeecff; font-size:11px; font-weight:700; letter-spacing:.3px; margin-bottom:13px; }
    .main-sub { font-size:14px; color:#7d89a0; margin:11px 0 0; }
    .welcome-card { margin:35px 0 22px; position:relative; overflow:hidden; border-radius:24px; padding:28px 30px; background:linear-gradient(115deg,#fff 0%,#f1efff 65%,#e7f7fb 100%); border:1px solid #e9e8f7; }
    .welcome-card:after { content:'✦'; position:absolute; right:35px; top:-28px; color:#8275eb22; font-size:160px; transform:rotate(12deg); }
    .welcome-kicker { color:#786be2; font-size:11px; font-weight:700; letter-spacing:1.1px; text-transform:uppercase; }
    .welcome-title { position:relative; z-index:1; font:700 21px 'Manrope',sans-serif; color:#27314b; margin:9px 0 7px; }
    .welcome-copy { position:relative; z-index:1; color:#76829a; font-size:13px; max-width:620px; line-height:1.7; margin:0; }
    .section-heading { color:#7b879f; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin:24px 0 9px; }
    .stButton > button { border-radius:13px; border:1px solid #e7eaf2; color:#3e4963; background:#fff; transition:all .18s ease; box-shadow:0 3px 12px #28335208; }
    .stButton > button:hover { border-color:#b8b0f5; color:#5e50d4; background:#fbfaff; transform:translateY(-1px); }
    [data-testid="stChatMessage"] { display:flex; align-items:flex-end; gap:10px; border:0; border-radius:0; background:transparent; padding:4px 0; margin:14px 0; box-shadow:none; }
    [data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) { flex-direction:row-reverse; }
    [data-testid="stChatMessageContent"] { flex:0 1 auto !important; width:auto !important; max-width:min(78%,680px) !important; margin:0 !important; padding:13px 17px !important; border:1px solid #e7eaf2; border-radius:18px 18px 18px 5px; background:#fff; box-shadow:0 5px 16px #2833520a; }
    [data-testid="stChatMessageContent"] p { color:#34405a; line-height:1.75; }
    [data-testid="stChatMessageContent"][aria-label="Chat message from user"] { border-color:transparent; border-radius:18px 18px 5px 18px; background:linear-gradient(135deg,#7566e8,#5a4bd0); }
    [data-testid="stChatMessageContent"][aria-label="Chat message from user"] p { color:#fff; }
    [data-testid="stChatMessageContent"][aria-label="Chat message from assistant"] { border-radius:18px 18px 18px 5px; }
    [data-testid="stChatInput"] { border-radius:17px; border:1px solid #e5e8f1; box-shadow:0 8px 30px #28335212; background:#fff; }
    [data-testid="stChatInput"] textarea { font-size:14px; }
    [data-testid="stChatInput"] button { color:#6759df; }
    [data-testid="stExpander"] { border:1px solid #e9edf5; border-radius:13px; background:#fbfcff; }
    .footer-note { text-align:center; color:#a2aabd; font-size:11px; margin-top:10px; }
    .upload-note { color:#828da2; font-size:11px; line-height:1.55; margin-top:-5px; }
    @media(max-width:700px) { .block-container{padding:1.3rem 1rem 6rem} .welcome-card{padding:22px 20px} .welcome-card:after{right:5px;font-size:110px} }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        '<div class="brand"><div class="brand-mark">✦</div><div><div class="brand-name">Ruang Tanya</div>'
        '<div class="brand-sub">Asisten dokumen kampus</div></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="side-label">Status layanan</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="status-card"><div class="status-row"><span class="status-dot"></span>Asisten siap membantu</div>'
        '<div class="status-note">Mode demo · jawaban menggunakan data simulasi</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="side-label">Basis pengetahuan</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Tambahkan dokumen PDF", type=["pdf"], accept_multiple_files=True,
        help="Unggah PDF untuk melihat nama file yang dipilih.", label_visibility="collapsed",
    )
    st.markdown(
        '<div class="upload-note">PDF dapat dipilih untuk demo. Indeks dokumen belum terhubung, jadi file tidak disimpan atau diproses.</div>',
        unsafe_allow_html=True,
    )
    if uploaded_files:
        st.caption(f"{len(uploaded_files)} file dipilih")
        for file in uploaded_files:
            st.caption(f"📄 {file.name}")
    st.divider()
    st.markdown('<div class="side-label">Percakapan</div>', unsafe_allow_html=True)
    if st.button("＋  Mulai percakapan baru", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.caption("Riwayat ini hanya tersimpan selama sesi berlangsung.")

st.markdown('<div class="main-eyebrow">✦ &nbsp; CHATBOT DOKUMEN CERDAS</div>', unsafe_allow_html=True)
st.title("Temukan jawaban dari dokumenmu")
st.markdown(
    '<p class="main-sub">Tanyakan hal yang ingin kamu ketahui. Jawaban dilengkapi referensi supaya mudah ditelusuri.</p>',
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

suggestions = [
    "Apa syarat mengajukan beasiswa?",
    "Bagaimana prosedur cuti akademik?",
    "Berapa IPK minimal untuk lulus?",
    "Dokumen apa untuk layanan administrasi?",
]
selected_prompt = None
if not st.session_state.messages:
    st.markdown(
        '<div class="welcome-card"><div class="welcome-kicker">Mulai dari sini</div>'
        '<div class="welcome-title">Halo! Ada yang ingin kamu cari tahu?</div>'
        '<p class="welcome-copy">Jelajahi informasi akademik dan administrasi dengan bahasa sehari-hari. Pilih pertanyaan cepat di bawah atau tulis pertanyaanmu sendiri.</p></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="section-heading">Coba tanyakan</div>', unsafe_allow_html=True)
    cols = st.columns(2, gap="small")
    for index, suggestion in enumerate(suggestions):
        with cols[index % 2]:
            if st.button(f"✧  {suggestion}", key=f"suggestion_{index}", use_container_width=True):
                selected_prompt = suggestion

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "🙂"):
        st.markdown(message["content"])
        sources = message.get("sources", [])
        if sources:
            with st.expander(f"📚  Referensi sumber · {len(sources)}"):
                for index, source in enumerate(sources, start=1):
                    title = source.get("title", "Dokumen")
                    filename = source.get("source", "Nama file tidak tersedia")
                    page = source.get("page", "—")
                    st.markdown(f"**{index}. {title}**  \n`{filename}` · Halaman {page}")

prompt = st.chat_input("Ketik pertanyaanmu di sini…")
if selected_prompt:
    prompt = selected_prompt

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})
    with st.chat_message("user", avatar="🙂"):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Menelusuri dokumen dan menyusun jawaban…"):
            try:
                result = tanya_rag(prompt)
                answer = result.get("jawaban", "Maaf, jawaban belum tersedia.")
                sources = result.get("sumber", [])
            except Exception as error:
                answer = "Maaf, asisten belum dapat memproses pertanyaan ini. Coba lagi sebentar lagi."
                sources = []
                st.error(f"Layanan tidak tersedia: {error}")
        st.markdown(answer)
        if sources:
            with st.expander(f"📚  Referensi sumber · {len(sources)}"):
                for index, source in enumerate(sources, start=1):
                    title = source.get("title", "Dokumen")
                    filename = source.get("source", "Nama file tidak tersedia")
                    page = source.get("page", "—")
                    st.markdown(f"**{index}. {title}**  \n`{filename}` · Halaman {page}")
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})

st.markdown('<div class="footer-note">Jawaban AI dapat keliru. Periksa kembali referensi dokumen yang disertakan.</div>', unsafe_allow_html=True)
