import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.title("Nama Aplikasi Kami")
nama = st.text_input("Ketik nama Anda di sini")

if st.button("Kirim"):
    if not nama:
        st.warning("Isi nama dulu ya")
    else:
        try:
            r = requests.get(f"{API_URL}/hello/{nama}", timeout=5)
            st.success(r.json()["pesan"])
        except requests.exceptions.ConnectionError:
            st.error("Backend belum berjalan. Jalankan uvicorn dulu.")