from fastapi import FastAPI

from app.routes import users, pasien, dokter, obat, tindakan, antrean, rekam_medis, pembayaran, detail_resep, detail_tindakan, views


app = FastAPI(
    title="Layanan Kesehatan API",
    description="Backend REST API untuk sistem layanan kesehatan",
    version="1.0.0"
)


app.include_router(users.router)
app.include_router(pasien.router)
app.include_router(dokter.router)
app.include_router(obat.router)
app.include_router(tindakan.router)
app.include_router(antrean.router)
app.include_router(rekam_medis.router)
app.include_router(pembayaran.router)
app.include_router(detail_resep.router)
app.include_router(detail_tindakan.router)
app.include_router(views.router)


@app.get("/")
def root():
    return {
        "message": "Layanan Kesehatan API berjalan"
    }