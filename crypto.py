"""Cryptography helpers for Guardian-Vault.

* Notes are ENCRYPTED with Fernet from the `cryptography` library
  (AES-128 in CBC mode, authenticated with HMAC-SHA256). Fernet adds a random
  IV to every message and rejects any ciphertext that has been tampered with.
* Passwords are never encrypted. They are HASHED with salted scrypt (through
  Werkzeug), so the original password cannot be recovered from the database.

The encryption key is read from the GUARDIAN_VAULT_KEY environment variable
and is never stored in the source code.
Generate a new key with:  python crypto.py
"""
import os

from cryptography.fernet import Fernet, InvalidToken
from werkzeug.security import check_password_hash, generate_password_hash


def generate_key():
    """Return a new random Fernet key as a string."""
    return Fernet.generate_key().decode("ascii")


def _fernet():
    key = os.environ.get("GUARDIAN_VAULT_KEY")
    if not key:
        raise RuntimeError(
            "GUARDIAN_VAULT_KEY is not set. Generate one with 'python crypto.py' "
            "and store it as an environment variable."
        )
    return Fernet(key.encode("ascii"))


def encrypt_text(plaintext):
    """Encrypt text and return a URL-safe string that can be saved in a file."""
    return _fernet().encrypt(plaintext.encode("utf-8")).decode("ascii")


def decrypt_text(token):
    """Decrypt text produced by encrypt_text.

    Raises ValueError if the data is not valid ciphertext, was modified, or was
    encrypted with a different key.
    """
    try:
        return _fernet().decrypt(token.strip().encode("ascii")).decode("utf-8")
    except (InvalidToken, UnicodeError) as exc:
        raise ValueError("Note could not be decrypted") from exc


def hash_password(password):
    """Return a salted scrypt hash of the password."""
    return generate_password_hash(password)


def verify_password(password, stored_hash):
    """Check a password against a stored hash."""
    try:
        return check_password_hash(stored_hash, password)
    except (ValueError, TypeError):
        return False


if __name__ == "__main__":
    print(generate_key())
