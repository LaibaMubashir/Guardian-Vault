# Guardian Vault - BITF20M025 & BITF20M020
import os
import re

from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename

import FileHandler
from crypto import decrypt_text, encrypt_text, hash_password
from DBHandle import DBHandler

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def require_env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} is not set. See README.md.")
    return value


app = Flask(__name__)
# Secrets are read from environment variables, never from the source code.
app.secret_key = require_env("FLASK_SECRET_KEY")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)


def get_db():
    return DBHandler(
        os.environ.get("DB_HOST", "localhost"),
        require_env("DB_USER"),
        require_env("DB_PASSWORD"),
        os.environ.get("DB_NAME", "guardianvault"),
    )


def note_path(email, noteName):
    """Path of a note file: <part of email before @>_<note name> in the notes folder."""
    return os.path.join(FileHandler.folder_path, email.split("@")[0] + "_" + noteName)


@app.route('/')
def sIn():
    return render_template("SignIn.html")


@app.route('/submitSignInForm', methods=["POST"])
def submitSignInForm():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if get_db().login(email, password):
        session['email'] = email
        return render_template("index.html")
    return render_template("SignIn.html", message="Email or Password is Incorrect")


@app.route('/signUp')
def sUp():
    # The sign-up form is part of SignIn.html (there is no separate SignUp.html).
    return render_template("SignIn.html")


@app.route('/submitSignUpForm', methods=["POST"])
def submitSignUpForm():
    name = request.form.get("FName", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    conPassword = request.form.get("conPassword", "")

    if not name or not EMAIL_PATTERN.match(email):
        return render_template("SignIn.html", message="Enter a valid name and email")
    if len(password) < 8 or len(conPassword) < 8:
        return render_template("SignIn.html", message="Password must be at least 8 characters long")
    if len(password) > 128:
        return render_template("SignIn.html", message="Password must be at most 128 characters long")
    if password != conPassword:
        return render_template("SignIn.html", message="Password not Match")

    # Only the salted hash of the password is stored, never the password itself.
    user = [name, email, hash_password(password)]
    if get_db().signUp(user):
        session['email'] = email
        return render_template("index.html")
    return render_template("SignIn.html", message="Email Already Exist")


@app.route('/Home', methods=['GET', 'POST'])
def new_page():
    if session.get('email'):
        return render_template('index.html')
    return render_template("SignIn.html", message="Log In First")


@app.route('/Note')
def note():
    if session.get('email'):
        return render_template('notes.html')
    return render_template("SignIn.html", message="Log In First")


@app.route('/NewNote', methods=['POST'])
def newNote():
    email = session.get('email')
    if not email:
        return render_template("SignIn.html", message="Log In First")

    # secure_filename removes path characters, so a note name cannot escape the notes folder.
    noteName = secure_filename(request.form.get("notesname", ""))
    note_input = request.form.get("noteInput", "")
    if not noteName or not note_input:
        return render_template('notes.html')

    try:
        filename = email.split("@")[0] + "_" + noteName
        own_notes = get_db().get_note_names_for_user(email)
        # Two emails can share the part before "@", so never overwrite a file that
        # belongs to another user.
        if noteName not in own_notes and os.path.exists(note_path(email, noteName)):
            return render_template("index.html", message="That note name is taken. Please choose another name.")
        # The note is encrypted before it is written to disk.
        if FileHandler.create_text_file(filename, encrypt_text(note_input)):
            if noteName not in own_notes:
                get_db().enterNoteName(email, noteName)
    except Exception as e:
        print("NewNote error:", e)
    return render_template("index.html")


@app.route('/MyNotes')
def mynotes():
    try:
        email = session.get('email')
        if not email:
            return render_template("SignIn.html", message="Log In First")

        # Only the notes recorded for this user in the database are read, in the same
        # order as their names, so each title is shown with its own text.
        files = get_db().get_note_names_for_user(email)
        content = []
        for name in files:
            try:
                content.append(decrypt_text(FileHandler.display_file_content(note_path(email, name))))
            except ValueError:
                content.append("[This note could not be decrypted]")

        if files != []:
            return render_template('about.html', file=files, cont=content, leng=len(files))
        return render_template('about.html', message="Create A New Note Right Now!", file=[])
    except Exception as e:
        print("MyNotes error:", e)
        return render_template("index.html")


@app.route('/deleteNotes')
def delete():
    email = session.get('email')
    if not email:
        return render_template("SignIn.html", message="Log In First")
    db = get_db()
    # Only delete the files of notes that belong to this user.
    for name in db.get_note_names_for_user(email):
        try:
            os.remove(note_path(email, name))
        except FileNotFoundError:
            pass
    if db.delete_all_notes_for_user(email):
        return render_template('about.html', message="Create A New Note Right Now!", file=[])
    return render_template("index.html")


@app.route('/logout')
def logout():
    session.clear()
    return render_template('SignIn.html')


if __name__ == "__main__":
    app.run()
