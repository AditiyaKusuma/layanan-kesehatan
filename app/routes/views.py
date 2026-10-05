from fastapi import APIRouter
from app.database import get_connection

router = APIRouter(
    prefix="/views",
    tags=["Database Views"]
)


@router.get("/antrean-hari-ini")
def get_antrean_hari_ini():
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_antrean,
                tgl_berobat,
                no_antrean,
                id_pasien,
                nama_pasien,
                id_dokter,
                nama_dokter,
                spesialisasi,
                estimasi_jam,
                status_antrean,
                prioritas
            FROM v_antrean_hari_ini
        """)

        return {
            "status": "success",
            "data": cursor.fetchall()
        }

    finally:
        cursor.close()
        connection.close()
        
@router.get("/riwayat-rekam-medis")
def get_riwayat_rekam_medis():
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_rekam_medis,
                waktu_pemeriksaan,
                id_pasien,
                nama_pasien,
                umur,
                id_dokter,
                nama_dokter,
                spesialisasi,
                keluhan,
                diagnosis
            FROM v_riwayat_rekam_medis
        """)

        return {
            "status": "success",
            "data": cursor.fetchall()
        }

    finally:
        cursor.close()
        connection.close()

@router.get("/tagihan-pasien")
def get_tagihan_pasien():
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_rekam_medis,
                id_pasien,
                nama_pasien,
                id_dokter,
                nama_dokter,
                total_tagihan,
                jumlah_dibayar,
                kembalian,
                metode_pembayaran,
                status_pembayaran,
                waktu_pembayaran
            FROM v_tagihan_pasien
        """)

        return {
            "status": "success",
            "data": cursor.fetchall()
        }

    finally:
        cursor.close()
        connection.close()