import streamlit as st
from rag_engine import tanya_rag

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Asisten Dokumen RAG - Produk B",
    page_icon="📚",
    layout="wide",
)
st.title("📚 Asisten Cerdas Berbasis Dokumen (Citation-Backed RAG)")
st.caption(
    "Ajukan pertanyaan seputar dokumen pedoman. Setiap jawaban dilengkapi referensi sumber dan halaman."
)

# 2. Sidebar: Informasi & Upload Dokumen (Untuk Uji Data Hold-Out)
with st.sidebar:
    st.header("📂 Manajemen Dokumen")
    st.info("Status Mesin: **Mode Simulasi UI**")

    uploaded_files = st.file_uploader(
        "Unggah Dokumen PDF Baru",
        type=["pdf"],
        accept_multiple_files=True,
        help="Digunakan untuk menambahkan dokumen baru ke basis pengetahuan.",
    )

    if uploaded_files:
        if st.button("Proses & Simpan ke Database", use_container_width=True):
            with st.spinner("Memproses ekstraksi teks & metadata PDF..."):
                # Nanti dihubungkan ke fungsi ingest dari Tim Model
                st.success(f"{len(uploaded_files)} dokumen berhasil ditambahkan!")

    st.divider()
    if st.button("🗑️ Bersihkan Riwayat Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 3. Inisialisasi Riwayat Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Halo! Silakan tanyakan informasi apa pun yang ada di dalam dokumen pedoman.",
            "sources": [],
        }
    ]

# 4. Menampilkan Riwayat Percakapan
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        # Tampilkan kotak sitasi jika ada sumber referensi
        if msg.get("sources"):
            with st.expander("📄 Lihat Sumber Referensi & Halaman"):
                for idx, src in enumerate(msg["sources"], start=1):
                    st.markdown(
                        f"**{idx}. {src['title']}**  \n"
                        f"File: `{src['source']}` | **Halaman {src['page']}**"
                    )

# 5. Input Pertanyaan Pengguna
if prompt := st.chat_input("Ketik pertanyaan Anda di sini..."):
    # Tampilkan pesan pengguna
    st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Proses jawaban dari RAG Engine
    with st.chat_message("assistant"):
        with st.spinner("Mencari referensi dari dokumen..."):
            hasil = tanya_rag(prompt)
            jawaban = hasil["jawaban"]
            sumber = hasil["sumber"]

            st.markdown(jawaban)
            if sumber:
                with st.expander("📄 Lihat Sumber Referensi & Halaman"):
                    for idx, src in enumerate(sumber, start=1):
                        st.markdown(
                            f"**{idx}. {src['title']}**  \n"
                            f"File: `{src['source']}` | **Halaman {src['page']}**"
                        )

    # Simpan respons ke riwayat
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": jawaban,
            "sources": sumber,
        }
    )
