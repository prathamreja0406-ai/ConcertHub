
import hashlib
import hmac
import secrets
from datetime import datetime

from app.database import get_connection
from app.validators import (
    validate_name,
    validate_email,
    validate_password
)


HASH_ITERATIONS = 120_000


def hash_password(password: str, salt: bytes = None):
    """
    Create a secure password hash using PBKDF2-HMAC-SHA256.
    """

    if salt is None:
        salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        HASH_ITERATIONS
    )

    return (
        salt.hex(),
        password_hash.hex()
    )


def verify_password(password: str, salt_hex: str, stored_hash: str):
    """
    Verify a password against its stored salt and hash.
    """

    salt = bytes.fromhex(salt_hex)

    _, calculated_hash = hash_password(
        password,
        salt
    )

    return hmac.compare_digest(
        calculated_hash,
        stored_hash
    )


def register_user(name, email, password, role="user"):

    name = validate_name(name)
    email = validate_email(email)
    password = validate_password(password)

    if role not in {"user", "admin"}:
        raise ValueError("Invalid user role.")

    salt, password_hash = hash_password(password)

    connection = get_connection()

    try:

        connection.execute("""
            INSERT INTO users (
                name,
                email,
                password_hash,
                password_salt,
                role,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            email,
            password_hash,
            salt,
            role,
            datetime.now().isoformat(timespec="seconds")
        ))

        connection.commit()

        return True, "Account created successfully."

    except Exception as error:

        connection.rollback()

        if "UNIQUE constraint failed" in str(error):
            return False, "An account with this email already exists."

        return False, "Unable to create account."

    finally:
        connection.close()


def login_user(email, password):

    email = validate_email(email)

    connection = get_connection()

    try:

        user = connection.execute("""
            SELECT
                user_id,
                name,
                email,
                password_hash,
                password_salt,
                role
            FROM users
            WHERE email = ?
        """, (email,)).fetchone()

        if not user:
            return None

        password_valid = verify_password(
            password,
            user["password_salt"],
            user["password_hash"]
        )

        if not password_valid:
            return None

        return {
            "user_id": user["user_id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }

    finally:
        connection.close()
