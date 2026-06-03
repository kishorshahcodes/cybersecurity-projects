"""
Encryption & Decryption Tool
Author: [Your Name]
Description: Implements classic and modern cipher techniques for learning cryptography.
             Supports Caesar, Vigenère, ROT13, XOR, and Base64.
"""

import base64
import argparse
import sys


# ─────────────────────────────────────────
# CAESAR CIPHER
# ─────────────────────────────────────────

def caesar_encrypt(text, shift):
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


def caesar_brute_force(ciphertext):
    """Try all 25 possible Caesar shifts."""
    print("\n🔓 Caesar Brute Force — All Possible Shifts:")
    print("-" * 50)
    for shift in range(1, 26):
        decrypted = caesar_decrypt(ciphertext, shift)
        print(f"  Shift {shift:>2}: {decrypted}")
    print("-" * 50)


# ─────────────────────────────────────────
# ROT13
# ─────────────────────────────────────────

def rot13(text):
    """ROT13 is its own inverse (special case of Caesar with shift=13)."""
    return caesar_encrypt(text, 13)


# ─────────────────────────────────────────
# VIGENÈRE CIPHER
# ─────────────────────────────────────────

def vigenere_encrypt(text, key):
    key = key.upper()
    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)


def vigenere_decrypt(text, key):
    key = key.upper()
    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base - shift) % 26 + base))
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)


# ─────────────────────────────────────────
# XOR CIPHER
# ─────────────────────────────────────────

def xor_cipher(text, key):
    """XOR encryption (symmetric — same function encrypts and decrypts)."""
    key_bytes = key.encode('utf-8')
    text_bytes = text.encode('utf-8')
    result = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(text_bytes)])
    return result.hex()


def xor_decrypt(hex_text, key):
    key_bytes = key.encode('utf-8')
    text_bytes = bytes.fromhex(hex_text)
    result = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(text_bytes)])
    return result.decode('utf-8', errors='replace')


# ─────────────────────────────────────────
# BASE64 ENCODING
# ─────────────────────────────────────────

def base64_encode(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')


def base64_decode(text):
    try:
        return base64.b64decode(text.encode('utf-8')).decode('utf-8')
    except Exception as e:
        return f"Error: {e}"


# ─────────────────────────────────────────
# INTERACTIVE MENU
# ─────────────────────────────────────────

def interactive_menu():
    print("""
╔════════════════════════════════════════╗
║     🔒 CRYPTOGRAPHY TOOL v1.0         ║
╚════════════════════════════════════════╝

 Ciphers Available:
  1. Caesar Cipher
  2. ROT13
  3. Vigenère Cipher
  4. XOR Cipher
  5. Base64 Encode/Decode
  6. Caesar Brute Force
  0. Exit
""")

    while True:
        choice = input("Select option: ").strip()

        if choice == '0':
            print("\n🔒 Stay curious, stay secure!\n")
            break

        elif choice == '1':
            text = input("Enter text: ")
            shift = int(input("Enter shift (1-25): "))
            action = input("(E)ncrypt or (D)ecrypt? ").strip().upper()
            if action == 'E':
                print(f"\n✅ Encrypted: {caesar_encrypt(text, shift)}\n")
            else:
                print(f"\n✅ Decrypted: {caesar_decrypt(text, shift)}\n")

        elif choice == '2':
            text = input("Enter text: ")
            print(f"\n✅ ROT13 Result: {rot13(text)}\n")

        elif choice == '3':
            text = input("Enter text: ")
            key = input("Enter keyword: ")
            action = input("(E)ncrypt or (D)ecrypt? ").strip().upper()
            if action == 'E':
                print(f"\n✅ Encrypted: {vigenere_encrypt(text, key)}\n")
            else:
                print(f"\n✅ Decrypted: {vigenere_decrypt(text, key)}\n")

        elif choice == '4':
            text = input("Enter text (or hex for decrypt): ")
            key = input("Enter XOR key: ")
            action = input("(E)ncrypt or (D)ecrypt? ").strip().upper()
            if action == 'E':
                print(f"\n✅ XOR Encrypted (hex): {xor_cipher(text, key)}\n")
            else:
                print(f"\n✅ XOR Decrypted: {xor_decrypt(text, key)}\n")

        elif choice == '5':
            text = input("Enter text: ")
            action = input("(E)ncode or (D)ecode? ").strip().upper()
            if action == 'E':
                print(f"\n✅ Base64 Encoded: {base64_encode(text)}\n")
            else:
                print(f"\n✅ Base64 Decoded: {base64_decode(text)}\n")

        elif choice == '6':
            text = input("Enter ciphertext: ")
            caesar_brute_force(text)

        else:
            print("❌ Invalid option. Try again.\n")


if __name__ == "__main__":
    interactive_menu()
