from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import get_connection


router = APIRouter(
    prefix="/detail-tindakan",
    tags=["Detail Tindakan"]
)


class DetailTindakanCreate(BaseModel):
    id_rekam_medis: int
    id_tindakan: int


@router.get("/")
def get_detail_tindakan():
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_detail_tindakan,
                id_rekam_medis,
                id_tindakan,
                biaya_at_time
            FROM detail_tindakan
            ORDER BY id_detail_tindakan DESC
        """)

        return {
            "status": "success",
            "data": cursor.fetchall()
        }

    finally:
        cursor.close()
        connection.close()


@router.get("/{id_detail_tindakan}")
def get_detail_tindakan_by_id(id_detail_tindakan: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_detail_tindakan,
                id_rekam_medis,
                id_tindakan,
                biaya_at_time
            FROM detail_tindakan
            WHERE id_detail_tindakan = %s
        """, (id_detail_tindakan,))

        detail = cursor.fetchone()

        if detail is None:
            raise HTTPException(
                status_code=404,
                detail="Detail tindakan tidak ditemukan"
            )

        return {
            "status": "success",
            "data": detail
        }

    finally:
        cursor.close()
        connection.close()


@router.post("/")
def create_detail_tindakan(data: DetailTindakanCreate):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        # Cek rekam medis
        cursor.execute("""
            SELECT id_rekam_medis
            FROM rekam_medis
            WHERE id_rekam_medis = %s
        """, (data.id_rekam_medis,))

        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=404,
                detail="Rekam medis tidak ditemukan"
            )

        # Ambil tarif tindakan
        cursor.execute("""
            SELECT
                id_tindakan,
                nama_tindakan,
                tarif
            FROM tindakan
            WHERE id_tindakan = %s
        """, (data.id_tindakan,))

        tindakan = cursor.fetchone()

        if tindakan is None:
            raise HTTPException(
                status_code=404,
                detail="Tindakan tidak ditemukan"
            )

        # Simpan detail tindakan
        cursor.execute("""
            INSERT INTO detail_tindakan (
                id_rekam_medis,
                id_tindakan,
                biaya_at_time
            )
            VALUES (%s, %s, %s)
        """, (
            data.id_rekam_medis,
            data.id_tindakan,
            tindakan["tarif"]
        ))

        connection.commit()

        return {
            "status": "success",
            "message": "Detail tindakan berhasil ditambahkan",
            "id_detail_tindakan": cursor.lastrowid,
            "biaya_at_time": tindakan["tarif"]
        }

    except HTTPException:
        connection.rollback()
        raise

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