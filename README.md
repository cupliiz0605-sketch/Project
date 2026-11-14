# Project

> Deskripsi singkat aplikasi: apa fungsinya dan masalah apa yang diselesaikan.

## Tim Pengembang

| Isi Nama | Username GitHub | Peran tiap anggota |
|---|---|---|
| Nama Ketua | @username | Ketua / PIC |
| Nama Anggota 2 | @username | Backend |
| Nama Anggota 3 | @username | Frontend |

## Tech Stack

| Lapisan | Teknologi |
|---|---|
| API (backend) | FastAPI |
| UI (frontend) | Streamlit / Web UI *(sesuai keputusan tim)* |
| Bahasa | Python 3.13 |

Keputusan teknis lengkap: [`docs/keputusan-teknis.md`](docs/keputusan-teknis.md)

> **Catatan versi Python:** gunakan **Python 3.13**. Python 3.15 terlalu baru dan beberapa library (misalnya `pyyaml`) gagal dipasang di dalamnya.

## Struktur Folder

```
Project/
├── backend/
│   ├── __init__.py
│   └── main.py
├── frontend/
│   └── app.py
├── docs/
│   └── keputusan-teknis.md
├── .github/
│   └── pull_request_template.md
├── .gitignore
├── requirements.txt
└── README.md
```

## Instalasi (Windows)

```bash
# 1. Clone repositori
git clone https://github.com/cupliiz0605-sketch/Project.git
cd Project

# 2. Pindah ke branch dev
git checkout dev

# 3. Buat dan aktifkan virtual environment
py -3.13 -m venv venv
venv\Scripts\activate

# 4. Instal dependensi
pip install -r requirements.txt
```

Mac/Linux: aktifkan venv dengan `source venv/bin/activate`.

## Menjalankan Aplikasi

Buka **dua terminal** dari folder utama proyek (`Project`), aktifkan venv di masing-masing.

**Terminal 1: Backend (FastAPI)**
```bash
uvicorn backend.main:app --reload
```
Dokumentasi API (Swagger): http://127.0.0.1:8000/docs

**Terminal 2: Frontend (Streamlit)**
```bash
streamlit run frontend/app.py
```
Aplikasi: http://localhost:8501

Menghentikan program: tekan `Ctrl + C` di terminal yang bersangkutan.

## Aturan Kontribusi

### 1. Skema Branch

| Branch | Fungsi |
|---|---|
| `main` | Kode stabil, siap rilis/demo. **Dilarang push langsung.** |
| `dev` | Integrasi semua fitur. **Dilarang push langsung.** |
| `feature/<nama-fitur>` | Pengerjaan fitur baru |
| `fix/<nama-bug>` | Perbaikan bug |

Alur: `feature/xxx` → Pull Request → `dev` → Pull Request → `main`

### 2. Identitas Git (wajib)

Gunakan nama dan email yang sama dengan akun GitHub agar kontribusi tercatat:

```bash
git config --global user.name "Nama Lengkap"
git config --global user.email "email-akun-github@contoh.com"
```

### 3. Alur Kerja

```bash
git checkout dev
git pull origin dev
git checkout -b feature/nama-fitur

# ...kerjakan kode, simpan dengan Ctrl + S...

git add .
git commit -m "feat(api): tambah endpoint login"
git push -u origin feature/nama-fitur
```

Lalu buat Pull Request ke branch `dev` di GitHub.

### 4. Format Commit

Format: `tipe(ruang-lingkup): deskripsi singkat`

| Tipe | Kegunaan | Contoh |
|---|---|---|
| `feat` | Fitur baru | `feat(api): tambah endpoint /predict` |
| `fix` | Perbaikan bug | `fix(ui): perbaiki tombol submit` |
| `docs` | Dokumentasi | `docs: update README` |
| `style` | Format kode | `style: rapikan indentasi` |
| `refactor` | Perbaikan struktur kode | `refactor(model): pisahkan preprocessing` |
| `test` | Test | `test(api): tambah test login` |
| `chore` | Dependensi/config | `chore: tambah fastapi ke requirements` |

Aturan:
- Commit kecil dan sering, satu commit untuk satu perubahan logis.
- Pesan commit singkat (maks. ±72 karakter), menggunakan kata kerja aktif.
- Jangan commit file sensitif (`.env`, API key, password) dan folder `venv/`.

### 5. Aturan Pull Request

- Judul PR mengikuti format commit.
- Deskripsi berisi: apa yang diubah, cara menguji, dan *screenshot* jika ada perubahan UI.
- Minimal **1 reviewer** menyetujui sebelum merge.
- Hapus branch fitur setelah merge.

## Kesepakatan API

- Format data: **JSON**
- Penamaan endpoint: huruf kecil, kata benda jamak (`/users`, `/predictions`)
- Metode HTTP: `GET`, `POST`, `PUT/PATCH`, `DELETE`
- Kode status: `200` OK, `201` Created, `400` Bad Request, `404` Not Found, `500` Server Error
- Semua endpoint terdokumentasi di Swagger (`/docs`)

## Kontak

Pertanyaan seputar repositori atau alur kerja: hubungi Ketua Tim di grup Tim Pengembang.