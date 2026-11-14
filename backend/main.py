from fastapi import FastAPI

app = FastAPI(title="API Aplikasi Kami")


@app.get("/")
def root():
    return {"status": "ok", "message": "API berjalan"}


@app.get("/hello/{nama}")
def hello(nama: str):
    return {"pesan": f"Selamat Datang, {nama}!"}