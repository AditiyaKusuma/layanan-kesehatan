import hashlib

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import get_connection


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


class UserCreate(BaseModel):
    username: str
    password: str
    role: str


@router.get("/")
def get_users():
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_user,
                username,
                password_hash,
                role
            FROM users
            ORDER BY id_user
        """)

        return {
            "status": "success",
            "data": cursor.fetchall()
        }

    finally:
        cursor.close()
        connection.close()


@router.get("/{id_user}")
def get_user_by_id(id_user: int):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_user,
                username,
                password_hash,
                role
            FROM users
            WHERE id_user = %s
        """, (id_user,))

        user = cursor.fetchone()

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User tidak ditemukan"
            )

        return {
            "status": "success",
            "data": user
        }

    finally:
        cursor.close()
        connection.close()


@router.post("/")
def create_user(data: UserCreate):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        # Cek username sudah digunakan atau belum
        cursor.execute("""
            SELECT id_user
            FROM users
            WHERE username = %s
        """, (data.username,))

        if cursor.fetchone() is not None:
            raise HTTPException(
                status_code=400,
                detail="Username sudah digunakan"
            )

        # Hash password
        password_hash = hashlib.sha256(
            data.password.encode("utf-8")
        ).hexdigest()

        cursor.execute("""
            INSERT INTO users (
                username,
                password_hash,
                role
            )
            VALUES (%s, %s, %s)
        """, (
            data.username,
            password_hash,
            data.role
        ))

        connection.commit()

        return {
            "status": "success",
            "message": "User berhasil ditambahkan",
            "id_user": cursor.lastrowid
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