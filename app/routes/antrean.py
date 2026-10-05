from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date

from app.database import get_connection


router = APIRouter(
    prefix="/antrean",
    tags=["Antrean"]
)


class AntreanCreate(BaseModel):
    id_pasien: int
    id_dokter: int
    tgl_berobat: date


# GET semua antrean
@router.get("/")
def get_antrean():
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_antrean,
                id_pasien,
                id_dokter,
                tgl_berobat,
                no_antrean,
                estimasi_jam,
                status_antrean,
                prioritas
            FROM antrean
            ORDER BY tgl_berobat DESC, no_antrean
        """)

        return {
            "status": "success",
            "data": cursor.fetchall()
        }

    finally:
        cursor.close()
        connection.close()


# GET antrean berdasarkan ID
@router.get("/{id_antrean}")
def get_antrean_by_id(id_antrean: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_antrean,
                id_pasien,
                id_dokter,
                tgl_berobat,
                no_antrean,
                estimasi_jam,
                status_antrean,
                prioritas
            FROM antrean
            WHERE id_antrean = %s
        """, (id_antrean,))

        antrean = cursor.fetchone()

        if antrean is None:
            raise HTTPException(
                status_code=404,
                detail="Antrean tidak ditemukan"
            )

        return {
            "status": "success",
            "data": antrean
        }

    finally:
        cursor.close()
        connection.close()


# POST membuat antrean melalui Stored Procedure
@router.post("/")
def create_antrean(data: AntreanCreate):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.callproc(
            "sp_daftar_antrean",
            (
                data.id_pasien,
                data.id_dokter,
                data.tgl_berobat
            )
        )

        hasil = None

        for result in cursor.stored_results():
            hasil = result.fetchall()

        connection.commit()

        return {
            "status": "success",
            "message": "Antrean berhasil didaftarkan",
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