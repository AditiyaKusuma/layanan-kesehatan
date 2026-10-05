from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from decimal import Decimal

from app.database import get_connection


router = APIRouter(
    prefix="/pembayaran",
    tags=["Pembayaran"]
)


class PembayaranCreate(BaseModel):
    id_rekam_medis: int
    metode_pembayaran: str
    jumlah_dibayar: Decimal


@router.get("/")
def get_pembayaran():
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_pembayaran,
                id_rekam_medis,
                total_tagihan,
                jumlah_dibayar,
                kembalian,
                metode_pembayaran,
                status_pembayaran,
                waktu_pembayaran
            FROM pembayaran
            ORDER BY id_pembayaran DESC
        """)

        return {
            "status": "success",
            "data": cursor.fetchall()
        }

    finally:
        cursor.close()
        connection.close()


@router.get("/{id_pembayaran}")
def get_pembayaran_by_id(id_pembayaran: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_pembayaran,
                id_rekam_medis,
                total_tagihan,
                jumlah_dibayar,
                kembalian,
                metode_pembayaran,
                status_pembayaran,
                waktu_pembayaran
            FROM pembayaran
            WHERE id_pembayaran = %s
        """, (id_pembayaran,))

        pembayaran = cursor.fetchone()

        if pembayaran is None:
            raise HTTPException(
                status_code=404,
                detail="Pembayaran tidak ditemukan"
            )

        return {
            "status": "success",
            "data": pembayaran
        }

    finally:
        cursor.close()
        connection.close()


@router.post("/")
def create_pembayaran(data: PembayaranCreate):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.callproc(
            "sp_buat_pembayaran",
            (
                data.id_rekam_medis,
                data.metode_pembayaran,
                data.jumlah_dibayar
            )
        )

        hasil = None

        for result in cursor.stored_results():
            hasil = result.fetchall()

        connection.commit()

        return {
            "status": "success",
            "message": "Pembayaran berhasil dibuat",
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