from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import get_connection


router = APIRouter(
    prefix="/obat",
    tags=["Obat"]
)


class ObatCreate(BaseModel):
    nama_obat: str
    kategori: str | None = None
    stok: int
    harga_satuan: float


@router.get("/")
def get_obat():
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_obat,
                nama_obat,
                kategori,
                stok,
                harga_satuan
            FROM obat
            ORDER BY id_obat
        """)

        return {
            "status": "success",
            "data": cursor.fetchall()
        }

    finally:
        cursor.close()
        connection.close()


@router.get("/{id_obat}")
def get_obat_by_id(id_obat: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_obat,
                nama_obat,
                kategori,
                stok,
                harga_satuan
            FROM obat
            WHERE id_obat = %s
        """, (id_obat,))

        obat = cursor.fetchone()

        if obat is None:
            raise HTTPException(
                status_code=404,
                detail="Obat tidak ditemukan"
            )

        return {
            "status": "success",
            "data": obat
        }

    finally:
        cursor.close()
        connection.close()


@router.post("/")
def create_obat(data: ObatCreate):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO obat (
                nama_obat,
                kategori,
                stok,
                harga_satuan
            )
            VALUES (%s, %s, %s, %s)
        """, (
            data.nama_obat,
            data.kategori,
            data.stok,
            data.harga_satuan
        ))

        connection.commit()

        return {
            "status": "success",
            "message": "Obat berhasil ditambahkan",
            "id_obat": cursor.lastrowid
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