def caesar_encrypt(plaintext, shift):
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            encrypted_char = chr((ord(char) - base + shift) % 26 + base)
            ciphertext += encrypted_char
        else:
            ciphertext += char
    return ciphertext

def caesar_decrypt(ciphertext, shift):
    return caesar_encrypt(ciphertext, -shift)

