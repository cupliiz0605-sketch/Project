# Tutorial Anggota: Mengunggah Pekerjaan ke GitHub (Proyek Project)

Panduan untuk seluruh anggota Tim Pengembang Aplikasi agar bisa mengambil proyek, mengerjakan bagian masing-masing, dan mengunggahnya ke GitHub dengan alur yang sama.

**Repositori tim:** https://github.com/cupliiz0605-sketch/Project

## Gambaran Alur

Semua pekerjaan masuk lewat **Pull Request**. Dilarang push langsung ke `main` dan `dev`.

| Branch | Fungsi | Boleh push langsung? |
|---|---|---|
| `main` | Kode stabil, siap rilis/demo | Tidak |
| `dev` | Integrasi semua fitur | Tidak |
| `feature/nama-fitur` | Tempat kerja masing-masing anggota | Ya, milik sendiri |

```
feature/xxx  →  Pull Request  →  dev  →  Pull Request  →  main
```

Pekerjaan dibagi dua tempat: **terminal VS Code** (kode dan Git) dan **website GitHub di browser** (undangan, Pull Request, review).

## Bagian A: Persiapan (dilakukan sekali per anggota)

### Langkah 1: Punya Akun GitHub dan Terima Undangan

1. Buat akun di github.com jika belum punya, lalu kirim **username GitHub** Anda ke ketua tim di grup.
2. Ketua akan mengundang Anda ke repositori. Buka **email** atau ikon **lonceng notifikasi** di GitHub.
3. Klik **View invitation**, lalu **Accept invitation**.
4. Buka https://github.com/cupliiz0605-sketch/Project. Jika halaman terbuka tanpa error 404, Anda sudah bergabung.

### Langkah 2: Pasang Alat yang Dibutuhkan

| Alat | Unduh | Catatan |
|---|---|---|
| **Python 3.13** | python.org/downloads/windows | Pilih **Windows installer (64-bit)** berakhiran `.exe`. **Centang "Add python.exe to PATH"** saat instalasi. Jangan pakai Python 3.15, library `pyyaml` gagal terpasang |
| **Git** | git-scm.com | Pilihan default boleh dipakai |
| **VS Code** | code.visualstudio.com | Pasang juga ekstensi **Python** (Microsoft) |

Cek di terminal:

```
python --version
git --version
```

### Langkah 3: Atur Identitas Git (wajib)

Agar kontribusi Anda tercatat atas nama Anda, gunakan **email yang sama dengan akun GitHub**:

```
git config --global user.name "Nama Lengkap"
git config --global user.email "email-akun-github@contoh.com"
```

Cek hasilnya:

```
git config user.name
git config user.email
```

### Langkah 4: Ambil Proyek (git clone)

1. Buat atau pilih folder penyimpanan, misalnya `Documents`.
2. Di VS Code: **File → Open Folder** ke folder itu, lalu **Terminal → New Terminal**.
3. Ketik:

```
git clone https://github.com/cupliiz0605-sketch/Project.git
```

4. Saat pertama kali, muncul jendela login GitHub. Pilih **Sign in with your browser**, lalu klik **Authorize** di browser.
5. Buka folder hasil clone di VS Code: **File → Open Folder → Project → Select Folder**. Pilih **Yes, I trust the authors**.

Cek bahwa terminal berada di folder yang benar. Baris terakhir harus berakhir `...\Project>`.

### Langkah 5: Pindah ke Branch `dev`

```
git checkout dev
```

Jika muncul `pathspec 'dev' did not match`, jalankan dulu `git fetch origin`, lalu ulangi.

### Langkah 6: Siapkan Lingkungan Python (satu per satu)

```
py -3.13 -m venv venv
```

```
venv\Scripts\activate
```

```
pip install -r requirements.txt
```

Tanda berhasil: muncul `(venv)` di awal baris terminal, dan `pip install` diakhiri `Successfully installed ...`. Pesan `[notice]` tentang pip baru boleh diabaikan.

Pilih interpreter di VS Code: `Ctrl + Shift + P` → **Python: Select Interpreter** → pilih yang berlokasi di folder `venv`.

### Langkah 7: Uji Proyek Berjalan

Buka **dua terminal** (ikon **+** di panel terminal). Di masing-masing, aktifkan venv dulu.

| Terminal | Perintah | Buka di browser |
|---|---|---|
| 1 (backend) | `uvicorn backend.main:app --reload` | http://127.0.0.1:8000/docs |
| 2 (UI) | `streamlit run frontend/app.py` | http://localhost:8501 |

Jika pertama kali Streamlit menanyakan email, kosongkan lalu tekan **Enter**. Hentikan program dengan **Ctrl + C**.

## Bagian B: Alur Setiap Kali Mengerjakan Tugas

Ulangi langkah 1 sampai 9 setiap kali mulai tugas baru. Jalankan di folder `Project`, dan gunakan terminal yang tidak sedang menjalankan server.

### Langkah 1: Ambil Update Terbaru

```
git checkout dev
```

```
git pull origin dev
```

### Langkah 2: Buat Branch Kerja Sendiri

```
git checkout -b feature/nama-fitur
```

Contoh nama branch:

| Jenis pekerjaan | Contoh nama |
|---|---|
| Fitur baru | `feature/login-api`, `feature/halaman-dashboard` |
| Perbaikan bug | `fix/error-upload` |
| Dokumentasi | `feature/docs-keputusan-teknis` |

Gunakan huruf kecil dan tanda hubung, tanpa spasi. Nama branch sebaiknya berbeda dari anggota lain agar tidak bentrok.

### Langkah 3: Kerjakan Kode di VS Code

1. Buka file di panel **Explorer**, tulis atau ubah kodenya.
2. Simpan dengan **Ctrl + S**. Titik putih di tab file hilang jika sudah tersimpan.
3. Jalankan dan uji hasilnya (lihat Bagian A, Langkah 7).

Lokasi file yang umum dikerjakan:

| Tugas | File atau folder |
|---|---|
| Backend (API) | `backend/main.py`, `backend/routers/`, `backend/models/` |
| Frontend (UI) | `frontend/app.py` |
| Dokumentasi | `docs/`, `README.md` |
| Library baru | `requirements.txt` |

### Langkah 4: Cek Perubahan

```
git status
```

Periksa daftar merah (file yang berubah). Pastikan **`venv/` tidak muncul** dan tidak ada file rahasia seperti `.env`. Jika `venv/` muncul, buka `.gitignore`, tambahkan baris `venv/`, simpan, lalu ulangi `git status`.

### Langkah 5: Simpan Perubahan (commit)

```
git add .
```

```
git commit -m "feat(api): tambah endpoint login"
```

Format pesan commit: `tipe(ruang-lingkup): deskripsi singkat`

| Tipe | Kegunaan | Contoh |
|---|---|---|
| `feat` | Fitur baru | `feat(api): tambah endpoint /predict` |
| `fix` | Perbaikan bug | `fix(ui): perbaiki tombol submit` |
| `docs` | Dokumentasi | `docs: update README` |
| `style` | Format kode | `style: rapikan indentasi` |
| `refactor` | Perbaikan struktur kode | `refactor(model): pisahkan preprocessing` |
| `test` | Pengujian | `test(api): tambah test login` |
| `chore` | Dependensi atau konfigurasi | `chore: tambah library ke requirements` |

Commit kecil dan sering lebih baik daripada satu commit besar.

### Langkah 6: Kirim ke GitHub (push)

Pertama kali untuk branch ini:

```
git push -u origin feature/nama-fitur
```

Push berikutnya di branch yang sama cukup:

```
git push
```

Berhasil jika muncul tulisan seperti `[new branch] feature/nama-fitur -> feature/nama-fitur`.

### Langkah 7: Buat Pull Request (di browser)

1. Buka https://github.com/cupliiz0605-sketch/Project.
2. Klik tombol hijau **Compare & pull request** (di bagian atas halaman, muncul setelah push).
3. Periksa dua kotak di bagian atas:
   - **base: `dev`** (tujuan)
   - **compare: `feature/nama-fitur`** (branch Anda)
4. Jika base masih `main`, klik dan ganti menjadi **`dev`**.
5. Isi **judul** dengan format commit, misalnya `feat(api): endpoint login`.
6. Isi **deskripsi**: apa yang diubah, cara mengujinya, dan *screenshot* bila ada perubahan tampilan.
7. Di panel kanan, klik **Reviewers** dan pilih minimal satu anggota tim.
8. Klik **Create pull request**.

### Langkah 8: Review dan Merge

1. Reviewer membuka tab **Files changed**, memberi komentar bila perlu, lalu klik **Review changes → Approve**.
2. Jika ada permintaan revisi, perbaiki di branch yang sama:

```
git add .
git commit -m "fix(api): perbaiki validasi password"
git push
```

   Pull Request ter-update otomatis.

3. Setelah disetujui dan tidak ada konflik, klik **Merge pull request**, lalu **Confirm merge**.
4. Klik **Delete branch** setelah merge selesai.

### Langkah 9: Bersihkan dan Siap Tugas Berikutnya

```
git checkout dev
```

```
git pull origin dev
```

```
git branch -d feature/nama-fitur
```

Lalu kembali ke Langkah 1 untuk tugas berikutnya.

## Bagian C: Cara Alternatif Tanpa Mengetik Perintah (VS Code)

Panel **Source Control** (ikon cabang di sisi kiri VS Code) bisa menggantikan perintah Git:

| Pekerjaan | Cara di VS Code |
|---|---|
| Pindah branch | Klik nama branch di pojok kiri bawah, pilih branch tujuan |
| Buat branch baru | Klik nama branch, pilih **Create new branch...**, ketik nama |
| Melihat perubahan | Daftar file di panel Source Control, klik untuk melihat perbedaannya |
| Commit | Klik **+** di samping **Changes**, tulis pesan, klik **Commit** |
| Push | Klik **Publish Branch** (pertama kali) atau **Sync Changes** |
| Ambil update | Menu **...** → **Pull** |

Setelah **Publish Branch**, buat Pull Request di browser seperti pada Langkah 7.

## Bagian D: Mengunggah File Lewat Website GitHub (Hanya Darurat)

GitHub menyediakan tombol **Add file → Upload files** untuk mengunggah file lewat browser. Cara ini **tidak disarankan** untuk proyek tim ini karena:

- Branch `main` dan `dev` diproteksi, sehingga unggahan langsung ke sana ditolak.
- File dan folder bisa salah tempat dan sulit dilacak.
- Riwayat commit sulit mengikuti format tim.

Jika terpaksa: pada halaman unggah pilih **Create a new branch for this commit**, beri nama `feature/nama-fitur`, lalu buka Pull Request ke `dev`.

## Aturan Penting Tim

- **Dilarang** push langsung ke `main` atau `dev`. Selalu lewat branch `feature/...` dan Pull Request.
- **Dilarang** meng-commit `venv/`, `__pycache__/`, `.env`, password, atau API key.
- Satu branch untuk satu tugas. Jangan mengerjakan dua fitur berbeda dalam satu branch.
- Pesan commit mengikuti format `tipe(ruang-lingkup): deskripsi`.
- Kerjakan di folder hasil `git clone`, jangan menyalin file secara manual ke folder lain.
- Gunakan identitas Git sendiri, jangan meminjam akun anggota lain.
- Jalankan `git pull origin dev` sebelum membuat branch baru agar tidak ketinggalan.

## Masalah Umum dan Solusinya

| Pesan atau masalah | Penyebab | Solusi |
|---|---|---|
| `fatal: not a git repository` | Terminal tidak di folder hasil clone | Buka folder `Project` lewat **File → Open Folder**, buka terminal baru |
| `Author identity unknown` | Identitas Git belum diatur | Jalankan `git config --global user.name ...` dan `user.email ...`, lalu ulangi commit |
| `Permission denied` atau error `403` | Undangan belum diterima atau login akun salah | Terima undangan di GitHub, login ulang dengan akun yang benar |
| `repository not found` | Undangan belum diterima, atau alamat repositori salah | Terima undangan, salin ulang alamat dari tombol **Code** |
| Push ke `main` atau `dev` ditolak | Branch diproteksi | Push ke branch `feature/...`, lalu buat Pull Request |
| `pathspec 'dev' did not match` | Branch belum terunduh | Jalankan `git fetch origin`, lalu `git checkout dev` |
| `failed to push some refs` | Branch lokal ketinggalan dari GitHub | Jalankan `git pull origin dev`, selesaikan konflik jika ada, lalu push ulang |
| `Failed building wheel for pyyaml` | Python terlalu baru (3.15) | Pakai Python 3.13, buat ulang `venv` |
| `'uvicorn' is not recognized` | `venv` belum aktif atau library belum terpasang | Aktifkan `venv`, jalankan `pip install -r requirements.txt` |
| `File does not exist: app.py` | Jalur Streamlit kurang `frontend/` | Jalankan `streamlit run frontend/app.py` |
| `venv/` ikut muncul di `git status` | `.gitignore` belum memuat `venv/` | Tambahkan `venv/` ke `.gitignore`, simpan, ulangi `git status` |
| `nothing to commit` | File belum disimpan atau sudah pernah di-commit | Simpan file dengan **Ctrl + S**, cek `git status` |
| Commit tidak masuk grafik kontribusi | Email Git berbeda dengan email akun GitHub | Samakan `user.email` dengan email akun GitHub |

### Menangani Konflik

Konflik terjadi jika dua orang mengubah baris yang sama. Selesaikan di branch Anda sendiri:

```
git checkout feature/nama-fitur
git pull origin dev
```

Jika muncul `CONFLICT`, buka file yang bermasalah di VS Code. Cari tanda `<<<<<<<`, `=======`, dan `>>>>>>>`, pilih kode yang benar (VS Code menyediakan tombol **Accept Current / Incoming / Both Changes**), lalu hapus tandanya. Setelah itu:

```
git add .
git commit -m "chore: selesaikan konflik dengan dev"
git push
```

## Checklist Anggota

- [ ] Akun GitHub dibuat, undangan repositori diterima
- [ ] Python 3.13, Git, dan VS Code terpasang
- [ ] Identitas Git (nama dan email akun GitHub) sudah diatur
- [ ] Repositori berhasil di-clone dan dibuka di VS Code
- [ ] `venv` aktif dan `pip install -r requirements.txt` berhasil
- [ ] Backend dan UI berhasil dijalankan di komputer sendiri
- [ ] Berhasil membuat branch `feature/...`, commit, dan push
- [ ] Berhasil membuat Pull Request ke `dev`
- [ ] Pull Request disetujui reviewer dan di-merge
- [ ] Kontribusi muncul di GitHub: **Insights → Contributors**

## Ringkasan Singkat (untuk Ditempel di Grup)

```
1. git checkout dev
2. git pull origin dev
3. git checkout -b feature/nama-fitur
4. Kerjakan kode → simpan (Ctrl + S)
5. git add .
6. git commit -m "feat(api): deskripsi singkat"
7. git push -u origin feature/nama-fitur
8. Buka GitHub → Compare & pull request → base: dev
9. Pilih reviewer → Create pull request
10. Setelah disetujui → Merge → Delete branch
11. git checkout dev && git pull origin dev
```
