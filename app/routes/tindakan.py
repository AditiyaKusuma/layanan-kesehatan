from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import get_connection


router = APIRouter(
    prefix="/tindakan",
    tags=["Tindakan"]
)


class TindakanCreate(BaseModel):
    nama_tindakan: str
    tarif: float


@router.get("/")
def get_tindakan():
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_tindakan,
                nama_tindakan,
                tarif
            FROM tindakan
            ORDER BY id_tindakan
        """)

        return {
            "status": "success",
            "data": cursor.fetchall()
        }

    finally:
        cursor.close()
        connection.close()


@router.get("/{id_tindakan}")
def get_tindakan_by_id(id_tindakan: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_tindakan,
                nama_tindakan,
                tarif
            FROM tindakan
            WHERE id_tindakan = %s
        """, (id_tindakan,))

        tindakan = cursor.fetchone()

        if tindakan is None:
            raise HTTPException(
                status_code=404,
                detail="Tindakan tidak ditemukan"
            )

        return {
            "status": "success",
            "data": tindakan
        }

    finally:
        cursor.close()
        connection.close()


@router.post("/")
def create_tindakan(data: TindakanCreate):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO tindakan (
                nama_tindakan,
                tarif
            )
            VALUES (%s, %s)
        """, (
            data.nama_tindakan,
            data.tarif
        ))

        connection.commit()

        return {
            "status": "success",
            "message": "Tindakan berhasil ditambahkan",
            "id_tindakan": cursor.lastrowid
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