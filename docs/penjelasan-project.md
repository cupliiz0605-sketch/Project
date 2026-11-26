# Penjelasan Project Chatbot Dokumen

Dokumen ini menjelaskan susunan project, alur chatbot, sintaks penting, kegunaan setiap bagian, dan alasan teknologi dipakai. File utama yang dijalankan menurut README adalah `frontend/app.py`.

## 1. Gambaran umum

Project ini berisi antarmuka chatbot berbasis Streamlit, fungsi mesin tanya-jawab simulasi, dan API FastAPI sederhana.

Alur chatbot saat ini:

1. Pengguna mengetik pertanyaan di `frontend/app.py` atau memilih tombol pertanyaan cepat.
2. Antarmuka memanggil `tanya_rag(pertanyaan)` dari `rag_engine.py`.
3. Mesin demo membuat sebuah dictionary berisi teks jawaban dan daftar sumber.
4. Streamlit menampilkan jawaban, menyimpan percakapan sementara di `st.session_state`, dan menyediakan panel sitasi.

> **Batasan penting:** `rag_engine.py` masih mock/simulasi. Ia tidak mencari isi PDF, tidak memakai model AI, dan sumber yang dikembalikan masih data contoh. Upload PDF pada `frontend/app.py` hanya menampilkan nama file yang dipilih; file belum diindeks atau disimpan.

## 2. Struktur folder

```text
Project/
├── app.py                       # UI Streamlit versi/prototipe lain
├── rag_engine.py                # Fungsi jawaban RAG simulasi
├── backend/
│   ├── __init__.py              # Penanda package Python
│   └── main.py                  # API FastAPI contoh
├── frontend/
│   └── app.py                   # UI chatbot yang dijalankan menurut README
├── docs/
│   ├── keputusan-teknis.md      # Catatan keputusan tim
│   └── penjelasan-project.md    # Penjelasan sintaks dan arsitektur ini
├── tests/
│   └── test_frontend.py         # Tes tampilan dan interaksi chatbot
├── requirements.txt             # Daftar library Python
└── README.md                    # Panduan instalasi dan menjalankan project
```

Folder `venv/`, `.git/`, dan `__pycache__/` dapat muncul secara lokal. Folder-folder itu bukan sumber utama aplikasi: `venv/` berisi library terpasang, `.git/` berisi riwayat Git, dan `__pycache__/` berisi bytecode sementara Python.

## 3. `frontend/app.py` — UI chatbot utama

### 3.1 Import dan mencari project root

```python
from pathlib import Path
import sys
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag_engine import tanya_rag
```

- `from ... import ...` mengambil fitur dari library/modul lain agar tidak perlu menulis ulang.
- `Path` membantu mengolah alamat file/folder lintas sistem operasi.
- `sys.path` adalah daftar lokasi yang dicari Python ketika melakukan `import`.
- `__file__` menunjuk file Python yang sedang dijalankan. `.resolve()` membuat lokasinya absolut; `.parent.parent` naik dari `frontend/` ke folder utama project.
- `if ... not in ...` mencegah folder root dimasukkan berulang kali. `sys.path.insert(0, ...)` menaruh root di urutan pencarian pertama supaya `rag_engine.py` ditemukan saat Streamlit menjalankan file dalam folder `frontend/`.
- `import streamlit as st` memberi nama singkat `st` untuk memanggil komponen Streamlit.
- `tanya_rag` adalah fungsi mesin jawaban demo.

### 3.2 Konfigurasi halaman

```python
st.set_page_config(
    page_title="Ruang Tanya · Asisten Dokumen",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)
```

- `st.set_page_config(...)` mengatur metadata dan layout halaman; letakkan sebelum perintah tampilan Streamlit lainnya.
- `page_title` menjadi judul tab browser.
- `page_icon` menjadi ikon tab.
- `layout="wide"` menggunakan ruang layar yang lebih lebar, berguna untuk area percakapan.
- `initial_sidebar_state="expanded"` membuka sidebar saat halaman pertama kali tampil.
- Tanda kurung, koma, dan indentasi membentuk pemanggilan fungsi Python dengan beberapa argumen bernama.

### 3.3 CSS dan HTML kustom

```python
st.markdown(""" ... CSS ... """, unsafe_allow_html=True)
```

- `st.markdown` menampilkan Markdown; parameter `unsafe_allow_html=True` mengizinkan HTML dan tag `<style>` di dalamnya.
- Tiga tanda petik (`"""`) membuat string multi-baris, sehingga aturan CSS bisa ditulis lebih mudah dibaca.
- `@import` mengambil font DM Sans dan Manrope dari Google Fonts; bila internet/font itu tidak tersedia, browser memakai font cadangan.
- CSS mengatur warna, jarak, border, bayangan, ukuran, dan perilaku responsif. Contohnya `background`, `padding`, `border-radius`, `font-size`, dan `@media`.
- Selector `[data-testid="stSidebar"]` dan `[data-testid="stChatMessage"]` memilih elemen Streamlit tertentu untuk diberi gaya. `:has(...)` memilih baris chat berdasarkan isi/atribut keturunannya.
- `flex-direction:row-reverse` membalik susunan baris pesan pengguna agar avatar dan bubble berada di sisi kanan. Pesan chatbot tetap memakai baris normal sehingga berada di kiri.
- `max-width` membatasi lebar bubble agar pesan panjang tetap mudah dibaca; `margin:0 !important` meniadakan margin otomatis bawaan Streamlit yang sebelumnya membuat kedua bubble tampak berpusat.
- Warna latar user ungu dan assistant putih membantu membedakan pengirim tanpa hanya mengandalkan posisi.
- HTML yang dimasukkan melalui `unsafe_allow_html=True` di sini adalah string UI buatan aplikasi. Hindari menyisipkan teks pengguna mentah sebagai HTML karena dapat membuka risiko XSS.

### 3.4 Sidebar: status, upload, dan percakapan baru

```python
with st.sidebar:
    ...
```

- `with` adalah context manager: semua perintah Streamlit yang diindentasi di dalamnya ditampilkan pada sidebar.
- `st.markdown(..., unsafe_allow_html=True)` dipakai untuk membuat logo, status layanan, dan keterangan dengan HTML/CSS.
- `st.file_uploader(..., type=["pdf"], accept_multiple_files=True)` menampilkan pemilih file PDF. `type` membatasi ekstensi, sedangkan `accept_multiple_files=True` mengizinkan beberapa file.
- `uploaded_files` berisi file yang dipilih selama sesi UI. Pada implementasi sekarang, file hanya ditampilkan namanya; belum ada proses ekstraksi teks/ingest.
- `if uploaded_files:` menjalankan blok hanya ketika setidaknya satu file dipilih. Di Python, koleksi kosong bernilai false dan koleksi berisi item bernilai true.
- `for file in uploaded_files:` mengulang tiap file agar nama setiap file dapat ditampilkan.
- `st.button(..., use_container_width=True)` membuat tombol selebar kontainer.
- Saat tombol percakapan baru diklik, `st.session_state.messages = []` mengosongkan riwayat lalu `st.rerun()` menjalankan ulang aplikasi agar tampilan langsung diperbarui.

### 3.5 Judul dan state percakapan

```python
st.title("Temukan jawaban dari dokumenmu")

if "messages" not in st.session_state:
    st.session_state.messages = []
```

- `st.title` menampilkan judul utama.
- `st.session_state` adalah tempat menyimpan data antar-rerun Streamlit dalam sesi pengguna yang sama.
- Streamlit menjalankan ulang script saat widget berubah; tanpa `session_state`, riwayat chat biasa akan hilang setiap kali ada interaksi.
- Kondisi `if "messages" not in ...` hanya membuat daftar kosong saat state belum ada, bukan menghapus percakapan pada setiap rerun.

### 3.6 Pertanyaan cepat

```python
suggestions = ["...", "..."]
selected_prompt = None

if not st.session_state.messages:
    cols = st.columns(2, gap="small")
    for index, suggestion in enumerate(suggestions):
        with cols[index % 2]:
            if st.button(suggestion, key=f"suggestion_{index}"):
                selected_prompt = suggestion
```

- `[...]` membuat list berurutan yang dapat berisi beberapa pertanyaan.
- `None` berarti belum ada pertanyaan yang dipilih.
- `if not ...` menampilkan panel sambutan dan saran hanya jika percakapan masih kosong.
- `st.columns(2)` membagi area menjadi dua kolom.
- `enumerate(...)` menghasilkan pasangan indeks dan isi, misalnya `(0, pertanyaan_pertama)`.
- `%` adalah operator sisa bagi. `index % 2` bergantian menghasilkan `0` dan `1`, sehingga tombol ditaruh berselang-seling di dua kolom.
- `key=f"suggestion_{index}"` memberi identitas unik pada setiap widget. `f"...{...}"` disebut f-string, cara menyisipkan nilai Python ke dalam string.
- Jika tombol dipilih, isi pertanyaan disimpan ke `selected_prompt` untuk diproses seperti input biasa.

### 3.7 Menampilkan riwayat dan referensi

```python
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="..."):
        st.markdown(message["content"])
        sources = message.get("sources", [])
```

- Pesan disimpan sebagai dictionary, misalnya `{"role": "user", "content": "...", "sources": []}`.
- `for` mengulang semua pesan yang tersimpan.
- `st.chat_message(...)` membuat blok chat. `role` membedakan `user` dan `assistant`; `avatar` memberi ikon emoji.
- `message["content"]` mengambil nilai wajib dari key `content`.
- `message.get("sources", [])` mengambil `sources`; jika key tidak ditemukan, hasilnya list kosong. Ini lebih aman daripada menganggap key itu selalu ada.
- `if sources:` memastikan panel referensi hanya muncul bila ada sumber.
- `st.expander(...)` membuat bagian referensi yang bisa dibuka/tutup agar chat tetap ringkas.
- `enumerate(sources, start=1)` memberi nomor mulai dari 1 untuk ditampilkan kepada pengguna.
- `source.get(...)` juga menyediakan nilai cadangan jika metadata seperti judul, nama file, atau halaman tidak tersedia.

### 3.8 Mengambil input dan meminta jawaban

```python
prompt = st.chat_input("Ketik pertanyaanmu di sini…")
if selected_prompt:
    prompt = selected_prompt

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})
    ...
```

- `st.chat_input` menampilkan kotak input chat dan mengembalikan teks saat pengguna mengirimnya.
- Pertanyaan dari tombol cepat menggantikan nilai input kosong lewat `if selected_prompt`.
- `if prompt:` mencegah pemrosesan string kosong.
- `.append(...)` menambahkan pesan pengguna ke akhir list riwayat.
- Dictionary memiliki key konsisten (`role`, `content`, `sources`) supaya fungsi tampilan bisa menangani user dan assistant dengan pola yang sama.

```python
with st.spinner("Menelusuri dokumen dan menyusun jawaban…"):
    try:
        result = tanya_rag(prompt)
        answer = result.get("jawaban", "Maaf, jawaban belum tersedia.")
        sources = result.get("sumber", [])
    except Exception as error:
        ...
```

- `st.spinner` menampilkan indikator proses selama fungsi jawaban berjalan.
- `try` menjalankan kode yang berpotensi gagal; `except` menampilkan respons cadangan bila terjadi exception.
- `as error` menyimpan detail exception ke variabel agar dapat ditampilkan untuk membantu diagnosis.
- `tanya_rag(prompt)` memanggil fungsi dengan pertanyaan sebagai argumen.
- Hasil fungsi adalah dictionary; `.get` mengambil jawaban dan sumber secara aman dengan nilai default.
- Setelah UI menampilkan jawaban, `.append(...)` menyimpan pesan assistant agar tetap ada pada rerun berikutnya.

## 4. `rag_engine.py` — mesin jawaban simulasi

```python
import time

def tanya_rag(pertanyaan: str) -> dict:
    ...
```

- `import time` mengambil fungsi waktu dari standard library Python.
- `def` mendefinisikan fungsi.
- `pertanyaan: str` adalah type hint: masukan yang diharapkan berupa teks.
- `-> dict` memberi petunjuk bahwa hasil fungsi berupa dictionary. Type hint membantu pembaca dan alat pemeriksa, tetapi Python tidak otomatis menolak tipe lain saat runtime.
- Docstring (`"""..."""`) menjelaskan tujuan fungsi.
- `time.sleep(1.5)` menunggu 1,5 detik untuk meniru jeda proses AI; ini bukan proses analisis dokumen.
- `pertanyaan.lower()` mengubah pertanyaan menjadi huruf kecil supaya pengecekan kata tidak peka huruf besar/kecil.
- `if "parkir" in ...` adalah contoh pertanyaan di luar konteks yang menghasilkan jawaban “tidak ditemukan” dan sumber kosong.
- `return` menghentikan fungsi dan mengirim nilai kembali ke pemanggil.
- Dictionary memakai pasangan `key: value`; list `[...]` dipakai untuk menyimpan banyak sumber.
- Sumber contoh memiliki `title`, `source`, dan `page`. Bentuk ini menjadi kontrak data yang dibaca antarmuka.
- Untuk RAG nyata, fungsi ini nantinya perlu diganti proses ingest dokumen, retrieval/pencarian potongan teks, pemanggilan model, dan pembentukan sitasi aktual.

## 5. `app.py` di root — UI/prototipe lain

`app.py` di folder utama juga merupakan aplikasi Streamlit terpisah. Berbeda dari `frontend/app.py`, tampilannya lebih sederhana dan menyatakan “Mode Simulasi UI”. Perintah menjalankannya adalah `streamlit run app.py`; README project saat ini mengarahkan penggunaan `frontend/app.py`.

- `import streamlit as st` memuat komponen Streamlit; `from rag_engine import tanya_rag` memuat fungsi jawaban yang sama.
- `st.set_page_config(...)` mengatur judul, ikon, dan layout.
- `with st.sidebar:` mengelompokkan kontrol dokumen dan tombol reset di sisi kiri.
- `st.file_uploader(..., type=["pdf"], accept_multiple_files=True)` menyediakan pemilih file.
- Tombol “Proses & Simpan ke Database” saat ini hanya menampilkan pesan sukses. Tidak ada kode ingest/database setelah diklik, jadi pesan itu tidak berarti file sudah diproses sungguhan.
- `st.session_state.messages` menyimpan riwayat. Di file ini, percakapan dimulai dengan pesan sambutan assistant.
- Sintaks `if prompt := st.chat_input(...):` memakai *walrus operator* `:=`: nilai input disimpan ke `prompt` sekaligus diuji apakah tidak kosong.
- `st.chat_message(msg["role"])` membuat area chat, lalu `st.markdown(...)` menampilkan isi pesan.
- `msg.get("sources")` mengecek apakah pesan punya sumber; `st.expander` membuka daftar file dan nomor halaman.
- Bagian pemrosesan memanggil `tanya_rag`, menampilkan jawaban, lalu menyimpan pesan assistant ke state.

## 6. `backend/main.py` — API FastAPI contoh

```python
from fastapi import FastAPI
app = FastAPI(title="API Aplikasi Kami")
```

- `FastAPI` adalah kelas dari library FastAPI.
- `app = FastAPI(...)` membuat objek aplikasi ASGI yang dipakai server Uvicorn.
- `title` menjadi nama API di dokumentasi otomatis.

```python
@app.get("/")
def root():
    return {"status": "ok", "message": "API berjalan"}
```

- `@app.get("/")` adalah decorator: mendaftarkan fungsi `root` sebagai handler HTTP GET pada alamat `/`.
- `def root()` mendefinisikan handler tanpa parameter.
- `return` mengirim dictionary; FastAPI mengubahnya menjadi respons JSON.

```python
@app.get("/hello/{nama}")
def hello(nama: str):
    return {"pesan": f"Selamat Datang, {nama}!"}
```

- `{nama}` pada path adalah parameter dinamis. FastAPI mengambil nilainya dari URL dan memasukkannya ke argumen `nama`.
- `nama: str` menyatakan nilai tersebut berupa teks.
- F-string menyisipkan nilai nama ke dalam respons.

Endpoint ini adalah demo terpisah; `frontend/app.py` sekarang memanggil `rag_engine.py` secara langsung dan belum menggunakan endpoint FastAPI tersebut.

## 7. File pendukung

### `backend/__init__.py`

File ini kosong. Kehadirannya menandai `backend` sebagai package Python tradisional sehingga modul di dalamnya dapat diimpor sebagai `backend.main`.

### `requirements.txt`

Setiap baris menyatakan satu dependensi yang dapat dipasang dengan `pip install -r requirements.txt`:

- `fastapi`: membuat HTTP API.
- `uvicorn[standard]`: menjalankan aplikasi ASGI FastAPI; `[standard]` meminta kumpulan dependensi tambahan yang umum dipakai Uvicorn.
- `streamlit`: membuat UI web Python.
- `requests`: library klien HTTP; pernah digunakan UI frontend prototipe untuk memanggil API.
- `pytest`: menjalankan tes otomatis.

### `tests/test_frontend.py`

- `Path(__file__).resolve().parents[1]` menghitung folder root project dari lokasi file tes.
- `AppTest.from_file(...)` menjalankan aplikasi Streamlit dalam harness tes, tanpa membuka browser manual.
- Setiap fungsi `test_...` adalah tes yang ditemukan pytest.
- `app.exception` diperiksa untuk memastikan aplikasi tidak gagal saat dirender atau digunakan.
- Tes awal memeriksa judul, kolom input, serta tombol pertanyaan cepat.
- Tes interaksi mengeklik saran pertama, lalu memeriksa state pesan dan nama sumber hasil.
- Tes alignment memastikan CSS mengatur pembalikan baris pengguna dan gaya khusus untuk kedua peran.
- `assert` membuat tes gagal bila kondisi yang diharapkan tidak benar.

### `README.md` dan `docs/keputusan-teknis.md`

- `README.md` adalah petunjuk instalasi, menjalankan aplikasi, struktur folder, dan aturan kontribusi.
- `docs/keputusan-teknis.md` adalah template catatan keputusan tim; beberapa nilai bertanda kurung siku masih perlu diisi oleh tim.

## 8. Menjalankan dan menguji

Dari terminal di folder root project pada Windows:

```bash
venv\Scripts\activate
streamlit run frontend/app.py
```

Buka `http://localhost:8501`. Untuk menjalankan API contoh secara terpisah:

```bash
uvicorn backend.main:app --reload
```

API dapat diuji melalui `http://127.0.0.1:8000/docs`. Untuk tes UI:

```bash
python -m pytest -q
```

Backend tidak harus berjalan untuk UI chatbot saat ini, karena `frontend/app.py` memanggil fungsi demo `tanya_rag` secara langsung. Menjalankan API hanya diperlukan bila sedang menguji endpoint FastAPI.
