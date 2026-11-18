# Guardian-Vault

A small Flask web application for storing confidential notes. Users sign up, sign in, and keep
notes that are encrypted before they are saved. Built as a university cybersecurity project at
PUCIT, University of the Punjab (BITF20M025 and BITF20M020), and later upgraded with modern
cryptography.

## Security design

| What | How it is protected |
|---|---|
| Notes | Encrypted with Fernet from the `cryptography` library (AES-128-CBC with HMAC-SHA256) before being written to disk. Each message gets a random IV, and modified data is rejected when decrypting. |
| Passwords | Never stored. Only a salted scrypt hash is kept, so the original password cannot be recovered. |
| Secrets | The encryption key, Flask secret key and database credentials come from environment variables, not from the source code. |
| Database | Every query is parameterised. A failed database call always means a failed login. |
| Note names | Cleaned with `secure_filename`, so a note name cannot point outside the notes folder. |
| Note access | A user can only read, overwrite or delete the notes recorded for their own account in the database. |
| Sessions | Cookies are `HttpOnly` and `SameSite=Lax`. |

## Setup

1. Create a virtual environment and install the dependencies:
   `python -m venv .venv`, activate it, then `pip install -r requirements.txt`
2. Create the database and tables in MySQL: `mysql -u root -p -e "source database.sql"`
3. Generate an encryption key: `python crypto.py`
4. Set the environment variables.

   Windows PowerShell:
   ```
   $env:GUARDIAN_VAULT_KEY = "<key from step 3>"
   $env:FLASK_SECRET_KEY = "<any long random string>"
   $env:DB_USER = "<mysql user>"
   $env:DB_PASSWORD = "<mysql password>"
   ```
   Linux or macOS: use `export NAME="value"` for the same four variables.
   Optional: `DB_HOST` (default `localhost`) and `DB_NAME` (default `guardianvault`).

5. Run the app: `python app.py`, then open http://127.0.0.1:5000

Encrypted notes are saved in the `Notes` folder, which is excluded from Git.
Keep the encryption key safe. Notes cannot be decrypted without it, and it must never be committed to Git.

## Tests

`python test_crypto.py` checks the encryption round trip, tamper detection, wrong-key handling and
password hashing.

## Known limitations

- One server-side key protects all notes. Anyone with access to both the server and the key can
  read them, so this is not end-to-end encryption.
- Forms have no CSRF tokens yet.
- There is no rate limiting or lockout on login attempts.
- Run it behind HTTPS and set `SESSION_COOKIE_SECURE=True` before using it outside a local machine.
- Email addresses are stored in plain text.
- Note files are named after the part of the email before "@", so two users with the same prefix
  cannot both use the same note name (the second user is asked to pick another name).
- The app has been tested by hand on Windows with MySQL 8.4; there are automated tests only for
  the cryptography helpers.

## Changelog

- **v2** Replaced the Caesar cipher with Fernet (AES) encryption. Passwords are now salted scrypt
  hashes instead of being stored in reversible form. Secrets moved out of the source code, SQL
  and file-name handling hardened, and a login bug fixed (a database error used to count as a
  successful login). Users can no longer see or delete each other's notes, and notes are saved
  in a `Notes` folder inside the project instead of a fixed path.
- **v1** First version, written for the university cybersecurity course.

The report, proposal and presentation PDFs in this repository document version 1.
