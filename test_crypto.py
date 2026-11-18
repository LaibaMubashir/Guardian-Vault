import os
import unittest

import crypto


class CryptoTests(unittest.TestCase):
    def setUp(self):
        os.environ["GUARDIAN_VAULT_KEY"] = crypto.generate_key()

    def test_round_trip(self):
        text = "bank PIN 4821, email: me@example.com"
        self.assertEqual(crypto.decrypt_text(crypto.encrypt_text(text)), text)

    def test_ciphertext_hides_plaintext(self):
        token = crypto.encrypt_text("secret note")
        self.assertNotIn("secret", token)

    def test_same_text_gives_different_ciphertext(self):
        self.assertNotEqual(crypto.encrypt_text("abc"), crypto.encrypt_text("abc"))

    def test_tampered_ciphertext_is_rejected(self):
        token = crypto.encrypt_text("secret note")
        tampered = token[:-4] + ("AAAA" if token[-4:] != "AAAA" else "BBBB")
        with self.assertRaises(ValueError):
            crypto.decrypt_text(tampered)

    def test_wrong_key_is_rejected(self):
        token = crypto.encrypt_text("secret note")
        os.environ["GUARDIAN_VAULT_KEY"] = crypto.generate_key()
        with self.assertRaises(ValueError):
            crypto.decrypt_text(token)

    def test_missing_key_raises(self):
        del os.environ["GUARDIAN_VAULT_KEY"]
        with self.assertRaises(RuntimeError):
            crypto.encrypt_text("x")

    def test_password_hash_and_verify(self):
        stored = crypto.hash_password("correct horse battery")
        self.assertNotIn("correct horse", stored)
        self.assertTrue(crypto.verify_password("correct horse battery", stored))
        self.assertFalse(crypto.verify_password("wrong password", stored))

    def test_password_hash_is_salted(self):
        self.assertNotEqual(crypto.hash_password("same"), crypto.hash_password("same"))


if __name__ == "__main__":
    unittest.main()
