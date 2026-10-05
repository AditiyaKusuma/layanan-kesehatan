from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import get_connection


router = APIRouter(
    prefix="/dokter",
    tags=["Dokter"]
)


class DokterCreate(BaseModel):
    id_user: int | None = None
    nama_dokter: str
    spesialisasi: str
    sip: str
    tarif_konsultasi: float


@router.get("/")
def get_dokter():
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_dokter,
                id_user,
                nama_dokter,
                spesialisasi,
                sip,
                tarif_konsultasi
            FROM dokter
            ORDER BY id_dokter
        """)

        return {
            "status": "success",
            "data": cursor.fetchall()
        }

    finally:
        cursor.close()
        connection.close()


@router.get("/{id_dokter}")
def get_dokter_by_id(id_dokter: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_dokter,
                id_user,
                nama_dokter,
                spesialisasi,
                sip,
                tarif_konsultasi
            FROM dokter
            WHERE id_dokter = %s
        """, (id_dokter,))

        dokter = cursor.fetchone()

        if dokter is None:
            raise HTTPException(
                status_code=404,
                detail="Dokter tidak ditemukan"
            )

        return {
            "status": "success",
            "data": dokter
        }

    finally:
        cursor.close()
        connection.close()


@router.post("/")
def create_dokter(data: DokterCreate):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO dokter (
                id_user,
                nama_dokter,
                spesialisasi,
                sip,
                tarif_konsultasi
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data.id_user,
            data.nama_dokter,
            data.spesialisasi,
            data.sip,
            data.tarif_konsultasi
        ))

        connection.commit()

        return {
            "status": "success",
            "message": "Dokter berhasil ditambahkan",
            "id_dokter": cursor.lastrowid
        }

    except Exception as e:
        connection.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    finally:
        cursor.close()
        connection.close()