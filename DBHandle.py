import pymysql

from crypto import hash_password, verify_password

# Checked when an email does not exist, so a login attempt takes about the same
# time whether or not the account exists.
_DUMMY_HASH = hash_password("not-a-real-password")


class DBHandler:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def _connect(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset="utf8mb4",
        )

    def login(self, email, password):
        """Return True only if the email exists and the password matches its stored hash."""
        mydb = None
        mydbCursor = None
        try:
            mydb = self._connect()
            mydbCursor = mydb.cursor()
            mydbCursor.execute("SELECT password FROM user WHERE email=%s", (email,))
            row = mydbCursor.fetchone()
            if row is None:
                verify_password(password, _DUMMY_HASH)
                return False
            return verify_password(password, row[0])
        except Exception as e:
            # Any error means the login fails.
            print("login error:", e)
            return False
        finally:
            if mydbCursor is not None:
                mydbCursor.close()
            if mydb is not None:
                mydb.close()

    def signUp(self, data):
        """data = [name, email, password_hash]. Returns True if the user was created."""
        mydb = None
        mydbCursor = None
        inserted = False
        try:
            mydb = self._connect()
            mydbCursor = mydb.cursor()
            mydbCursor.execute("SELECT id FROM user WHERE email=%s", (data[1],))
            if mydbCursor.fetchone() is None:
                mydbCursor.execute(
                    "INSERT INTO user (name, email, password) VALUES (%s, %s, %s)",
                    (data[0], data[1], data[2]),
                )
                mydb.commit()
                inserted = True
        except Exception as e:
            print("signUp error:", e)
        finally:
            if mydbCursor is not None:
                mydbCursor.close()
            if mydb is not None:
                mydb.close()
        return inserted

    def enterNoteName(self, email, noteName):
        """Save the name of a note against the user. Returns True on success."""
        mydb = None
        mydbCursor = None
        inserted = False
        try:
            mydb = self._connect()
            mydbCursor = mydb.cursor()
            mydbCursor.execute("SELECT id FROM user WHERE email=%s", (email,))
            row = mydbCursor.fetchone()
            if row:
                mydbCursor.execute(
                    "INSERT INTO notes (userid, notename) VALUES (%s, %s)",
                    (row[0], noteName),
                )
                mydb.commit()
                inserted = True
        except Exception as e:
            print("enterNoteName error:", e)
        finally:
            if mydbCursor is not None:
                mydbCursor.close()
            if mydb is not None:
                mydb.close()
        return inserted

    def get_note_names_for_user(self, email):
        mydb = None
        mydbCursor = None
        note_names = []
        try:
            mydb = self._connect()
            mydbCursor = mydb.cursor()
            mydbCursor.execute("SELECT id FROM user WHERE email=%s", (email,))
            row = mydbCursor.fetchone()
            if row:
                mydbCursor.execute("SELECT notename FROM notes WHERE userid=%s", (row[0],))
                note_names = [r[0] for r in mydbCursor.fetchall()]
        except Exception as e:
            print("get_note_names_for_user error:", e)
        finally:
            if mydbCursor is not None:
                mydbCursor.close()
            if mydb is not None:
                mydb.close()
        return note_names

    def delete_all_notes_for_user(self, email):
        """Delete the note names of a user. Returns True on success."""
        mydb = None
        mydbCursor = None
        deleted = False
        try:
            mydb = self._connect()
            mydbCursor = mydb.cursor()
            mydbCursor.execute("SELECT id FROM user WHERE email=%s", (email,))
            row = mydbCursor.fetchone()
            if row:
                mydbCursor.execute("DELETE FROM notes WHERE userid=%s", (row[0],))
                mydb.commit()
                deleted = True
        except Exception as e:
            print("delete_all_notes_for_user error:", e)
        finally:
            if mydbCursor is not None:
                mydbCursor.close()
            if mydb is not None:
                mydb.close()
        return deleted
