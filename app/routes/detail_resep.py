from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import get_connection


router = APIRouter(
    prefix="/detail-resep",
    tags=["Detail Resep"]
)


class DetailResepCreate(BaseModel):
    id_rekam_medis: int
    id_obat: int
    jumlah: int
    dosis: str


@router.get("/")
def get_detail_resep():
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_detail_resep,
                id_rekam_medis,
                id_obat,
                jumlah,
                dosis,
                harga_at_time
            FROM detail_resep
            ORDER BY id_detail_resep DESC
        """)

        return {
            "status": "success",
            "data": cursor.fetchall()
        }

    finally:
        cursor.close()
        connection.close()


@router.get("/{id_detail_resep}")
def get_detail_resep_by_id(id_detail_resep: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_detail_resep,
                id_rekam_medis,
                id_obat,
                jumlah,
                dosis,
                harga_at_time
            FROM detail_resep
            WHERE id_detail_resep = %s
        """, (id_detail_resep,))

        detail = cursor.fetchone()

        if detail is None:
            raise HTTPException(
                status_code=404,
                detail="Detail resep tidak ditemukan"
            )

        return {
            "status": "success",
            "data": detail
        }

    finally:
        cursor.close()
        connection.close()


@router.post("/")
def create_detail_resep(data: DetailResepCreate):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            INSERT INTO detail_resep (
                id_rekam_medis,
                id_obat,
                jumlah,
                dosis
            )
            VALUES (%s, %s, %s, %s)
        """, (
            data.id_rekam_medis,
            data.id_obat,
            data.jumlah,
            data.dosis
        ))

        connection.commit()

        return {
            "status": "success",
            "message": "Detail resep berhasil ditambahkan",
            "id_detail_resep": cursor.lastrowid
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