from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date

from app.database import get_connection


router = APIRouter(
    prefix="/pasien",
    tags=["Pasien"]
)


class PasienCreate(BaseModel):
    nik: str
    nama_pasien: str
    tgl_lahir: date
    jenis_kelamin: str
    no_telepon: str | None = None
    alamat: str | None = None
    id_user: int | None = None
    email: str | None = None


@router.get("/")
def get_pasien():
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_pasien,
                id_user,
                nik,
                nama_pasien,
                tgl_lahir,
                jenis_kelamin,
                no_telepon,
                alamat,
                email
            FROM pasien
            ORDER BY id_pasien
        """)

        return {
            "status": "success",
            "data": cursor.fetchall()
        }

    finally:
        cursor.close()
        connection.close()


@router.get("/{id_pasien}")
def get_pasien_by_id(id_pasien: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_pasien,
                id_user,
                nik,
                nama_pasien,
                tgl_lahir,
                jenis_kelamin,
                no_telepon,
                alamat,
                email
            FROM pasien
            WHERE id_pasien = %s
        """, (id_pasien,))

        pasien = cursor.fetchone()

        if pasien is None:
            raise HTTPException(
                status_code=404,
                detail="Pasien tidak ditemukan"
            )

        return {
            "status": "success",
            "data": pasien
        }

    finally:
        cursor.close()
        connection.close()


@router.post("/")
def create_pasien(data: PasienCreate):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO pasien (
                id_user,
                nik,
                nama_pasien,
                tgl_lahir,
                jenis_kelamin,
                no_telepon,
                alamat,
                email
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data.id_user,
            data.nik,
            data.nama_pasien,
            data.tgl_lahir,
            data.jenis_kelamin,
            data.no_telepon,
            data.alamat,
            data.email
        ))

        connection.commit()

        return {
            "status": "success",
            "message": "Pasien berhasil ditambahkan",
            "id_pasien": cursor.lastrowid
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
        
class PasienUserUpdate(BaseModel):
    id_user: int


@router.put("/{id_pasien}/user")
def update_pasien_user(id_pasien: int, data: PasienUserUpdate):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        # Cek pasien
        cursor.execute("""
            SELECT id_pasien
            FROM pasien
            WHERE id_pasien = %s
        """, (id_pasien,))

        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=404,
                detail="Pasien tidak ditemukan"
            )

        # Cek user
        cursor.execute("""
            SELECT id_user
            FROM users
            WHERE id_user = %s
        """, (data.id_user,))

        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=404,
                detail="User tidak ditemukan"
            )

        # Hubungkan user dengan pasien
        cursor.execute("""
            UPDATE pasien
            SET id_user = %s
            WHERE id_pasien = %s
        """, (data.id_user, id_pasien))

        connection.commit()

        return {
            "status": "success",
            "message": "User berhasil dihubungkan dengan pasien",
            "id_pasien": id_pasien,
            "id_user": data.id_user
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