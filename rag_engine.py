import time


def tanya_rag(pertanyaan: str) -> dict:
    """
    Fungsi simulasi (Mock) agar Tim Pengembang Aplikasi bisa langsung membangun UI.
    Nanti file ini akan diganti dengan rag_engine.py asli dari Tim Model & Analitik.
    """
    time.sleep(1.5)  # Simulasi proses AI berpikir

    # Simulasi skenario pertanyaan jebakan (Out-of-Context)
    if "parkir" in pertanyaan.lower():
        return {
            "jawaban": "Maaf, informasi tersebut tidak ditemukan di dalam dokumen yang tersedia.",
            "sumber": [],
        }

    # Simulasi skenario jawaban normal dengan sitasi sesuai kontrak Data Dictionary
    return {
        "jawaban": (
            f"Berdasarkan dokumen pedoman yang tersedia, jawaban untuk pertanyaan "
            f"'{pertanyaan}' adalah mahasiswa wajib memenuhi syarat administrasi "
            f"dan memiliki IPK minimal 3,00."
        ),
        "sumber": [
            {
                "title": "Buku Pedoman Akademik 2026",
                "source": "01_Pedoman_Akademik_2026.pdf",
                "page": 4,
            },
            {
                "title": "SOP Layanan Administrasi Mahasiswa",
                "source": "02_SOP_Administrasi_Mahasiswa.pdf",
                "page": 2,
            },
        ],
    }
