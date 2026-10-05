from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import get_connection


router = APIRouter(
    prefix="/rekam-medis",
    tags=["Rekam Medis"]
)


class RekamMedisCreate(BaseModel):
    id_antrean: int
    keluhan: str
    diagnosis: str


# GET semua rekam medis
@router.get("/")
def get_rekam_medis():
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_rekam_medis,
                id_antrean,
                id_pasien,
                id_dokter,
                waktu_pemeriksaan,
                keluhan,
                diagnosis
            FROM rekam_medis
            ORDER BY id_rekam_medis DESC
        """)

        return {
            "status": "success",
            "data": cursor.fetchall()
        }

    finally:
        cursor.close()
        connection.close()


# GET rekam medis berdasarkan ID
@router.get("/{id_rekam_medis}")
def get_rekam_medis_by_id(id_rekam_medis: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_rekam_medis,
                id_antrean,
                id_pasien,
                id_dokter,
                waktu_pemeriksaan,
                keluhan,
                diagnosis
            FROM rekam_medis
            WHERE id_rekam_medis = %s
        """, (id_rekam_medis,))

        rekam_medis = cursor.fetchone()

        if rekam_medis is None:
            raise HTTPException(
                status_code=404,
                detail="Rekam medis tidak ditemukan"
            )

        return {
            "status": "success",
            "data": rekam_medis
        }

    finally:
        cursor.close()
        connection.close()


# POST membuat rekam medis melalui Stored Procedure
@router.post("/")
def create_rekam_medis(data: RekamMedisCreate):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.callproc(
            "sp_buat_rekam_medis",
            (
                data.id_antrean,
                data.keluhan,
                data.diagnosis
            )
        )

        hasil = None

        for result in cursor.stored_results():
            hasil = result.fetchall()

        connection.commit()

        return {
            "status": "success",
            "message": "Rekam medis berhasil dibuat",
            "data": hasil
        }

    except Exception as e:
        connection.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()